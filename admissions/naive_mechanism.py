from .domain import AdmissionData, Allocation
from .mechanism import Mechanism


class NaiveMechanism(Mechanism):
    """
    Naivní mechanismus
    ------------------

    §60i Způsob hodnocení výsledků přijímacího řízení
    ...
    (2) Pokud splní kritéria přijímacího řízení více uchazečů než kolik lze přijmout,
    rozhoduje jejich pořadí podle výsledků hodnocení kritérií přijímacího řízení.
    (3) Umístí-li se uchazeč na místě opravňujícím k přijetí do více oborů středního
    vzdělání, bude přijat do oboru umístěného z těchto oborů středního vzdělání na
    přednostnějším pořadí uvedeném v přihlášce podle § 60b; do ostatních oborů středního
    vzdělání nebude uchazeč přijat.
    ...

    Doslovnému znění nejvíce odpovídá právě naivní mechanismus popsaný níže.

    Algoritmus:
    1. Ze všech žáků hlásících se na danou školu nabídni přijetí všem nad čarou.
    2. Každý žák je zapsán na nejlepší ze škol, na které je přijatý.
    3. Zapsaní žáci jsou vyřazeni, uvolní se místa a s dosud nezapsanými žáky
       se vše opakuje od kroku 1.
    """

    def __init__(self, data: AdmissionData):
        super().__init__(data)
        self.accepted = {s: set() for s in self.schools}
        self.remaining_seats = {s: x for s, x in self.seats.items()}
        self.remaining_applicants = {
            sch: [x for x in students] for sch, students in self.exams.items()
        }

    def is_done(self) -> bool:
        should_continue = False
        for school, applicants in self.remaining_applicants.items():
            vacant = self.remaining_seats[school]
            should_continue = should_continue or bool(applicants[:vacant])
        return not should_continue

    def step(self):
        # 1. projdi remaining_applicants a nad carou pridej do offers
        offers = {}
        for school, applicants in self.remaining_applicants.items():
            for st in applicants[: self.remaining_seats[school]]:
                if st in offers:
                    offers[st].append(school)
                else:
                    offers[st] = [school]
        # 2. prijmi na nejlepsi offer a odstran z remaining_applicants
        for st, offs in offers.items():
            for sch in self.applications[st]:
                if sch in offs:
                    self.accepted[sch].add(st)
                    break
        self.remaining_applicants = {
            sch: [st for st in sts if st not in offers]
            for sch, sts in self.remaining_applicants.items()
        }
        # 3. aktualizuj zbyvajici volna mista
        self.remaining_seats = {
            sch: self.seats[sch] - len(self.accepted[sch]) for sch in self.schools
        }
        # return logs
        return {
            "Current offers": offers,
            "Accepted": self.accepted,
            "Remaining applicants": self.remaining_applicants,
            "Remaining seats": self.remaining_seats,
        }

    def allocate(self) -> Allocation:
        accepted = {sch: frozenset(sts) for sch, sts in self.accepted.items()}
        all_accepted = {st for sts in self.accepted.values() for st in sts}
        rejected = self.students - all_accepted
        return Allocation(accepted=accepted, rejected=frozenset(rejected))
