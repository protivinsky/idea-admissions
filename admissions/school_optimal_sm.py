from typing import Dict, Any
from copy import deepcopy
from collections import defaultdict
from .domain import AdmissionData, Allocation
from .mechanism import Mechanism
from .logger import Logger


class SchoolOptimalSM(Mechanism):
    """
    Stabilní mechanismus optimální pro školy
    ----------------------------------------

    Mechanismus navržený Cermatem je ekvivalentní ke stabilnímu mechanismu optimálnímu
    pro školy. Školy by tedy preferovaly tuto verzi algoritmu, avšak pro studenty
    tento algoritmus není optimální a mohou dosáhnout lepšího stabilního výsledku
    při použití mechanismu odloženého přijetí.

    **Algoritmus**

    1. Podle výsledků zkoušky a vlastní kapacity každá škola stanoví,
        kteří žáci mají nárok na přijetí.
    2. Žáci s nárokem na přijetí jsou podmíněně přijati (pokud se následně nerozhodnou
        pro preferovanější školu) a z ostatních škol nad čarou jsou vyškrtnuti.
    3. Tím se na školách uvolní nová místa a přijímací hranici se posunou
        níže.
    4. Opakuje se od bodu 1, dokud zbývají žáci bez podmíněného přijetí a je možné
        pokračovat. Pokud v dalších kolech je žákům nabídnuta více preferovaná
        škola, mohou své rozhodnutí změnit.

    Tento algoritmus je analogický k deferred acceptance, pouze role škol a žáků
    je obrácená. DA prochází pořadí dle preferencí žáků a školy je podmíněně přijímají
    (nebo zcela odmítají). School-optimal SM prochází výsledky dle pořadí dle zkoušek
    ve školách a žáci buď nabídku přijetí podmíněně akceptují, nebo ji odmítají.

    Tento algoritmus je také velice podobný naivnímu, pouze přijetí žáků jsou pouze podmíněná
    a vyškrtnutí jsou pouze ze škol, kde oni sami odmítnuli přijetí (a bylo jim nabídnuto).
    """

    def __init__(self, data: AdmissionData, logger: Logger = Logger()):
        super().__init__(data, logger=logger)
        self.accepted = {sch: set() for sch in self.schools}
        self.remaining_seats = {sch: n for sch, n in self.seats.items()}
        self.remaining_applicants = {
            sch: [st for st in sts] for sch, sts in self.exams.items()
        }

    def is_done(self) -> bool:
        is_done = True
        for sch in self.schools:
            # school is not done when
            # - there are still some remaining applicant
            # - AND the school still have remaining seats
            school_not_done = (
                self.remaining_seats[sch] and self.remaining_applicants[sch]
            )
            is_done = is_done and not school_not_done
            if not is_done:
                break
        return is_done

    def step(self) -> Dict[str, Any]:
        # 1. new offers in this round (identical to naive mechanism here)
        offers = defaultdict(set)
        for sch, sts in self.remaining_applicants.items():
            for st in sts[: self.remaining_seats[sch]]:
                offers[st].add(sch)
        # 2. move already accepted to offers
        for sch, sts in self.accepted.items():
            for st in sts:
                offers[st].add(sch)
        self.accepted = {sch: set() for sch in self.schools}
        # 3. select the best offers
        for st, offered_schools in offers.items():
            for sch in self.applications[st]:
                # accept the best and continue with next student
                if sch in offered_schools:
                    self.accepted[sch].add(st)
                    break
        # 4. update remove the evaluated applicants from the remaining
        for sch in self.schools:
            self.remaining_applicants[sch] = self.remaining_applicants[sch][
                self.remaining_seats[sch] :
            ]
        # 5. update remaining seats
        for sch in self.schools:
            self.remaining_seats[sch] = self.seats[sch] - len(self.accepted[sch])
        # return logs
        return deepcopy(
            {
                "__name__": self.__class__.__name__,
                "Offers": offers,
                "Accepted": self.accepted,
                "Remaining applicants": self.remaining_applicants,
                "Remaining seats": self.remaining_seats,
            }
        )

    def allocate(self) -> Allocation:
        accepted = {sch: frozenset(sts) for sch, sts in self.accepted.items()}
        all_accepted = {st for sts in self.accepted.values() for st in sts}
        rejected = self.students - all_accepted
        return Allocation(accepted=accepted, rejected=frozenset(rejected))
