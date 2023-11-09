from .domain import Admission, Allocation
from .mechanism import Mechanism


class NaiveMechanism(Mechanism):
    """
    Naivní mechanismus
    ------------------

    TODO: add the quote from the law...

    Algoritmus:
    1. Ze všech žáků hlásících se na danou školu nabídni přijetí všem nad čarou.
    2. Každý žák je zapsán na nejlepší ze škol, na které je přijatý.
    3. Zapsaní žáci jsou vyřazeni, uvolní se místa a s dosud nezapsanými žáky
       se vše opakuje od kroku 1.
    """

    def __init__(self, data: Admission):
        super().__init__(data)
        self.accepted = {s: set() for s in self.schools}
        self.remaining_seats = {s: x for s, x in self.seats.items()}
        self.remaining_applicants = {
            sch: [x for x in students] for sch, students in self.exams.items()
        }
        # logging
        self.num_steps = 0  # this could live in logger
        self.offers = {}

    def log():
        ...

    def step(self):
        # 1. projdi remaining_applicants a nad carou pridej do offers
        self.offers = {}
        for school, applicants in self.remaining_applicants.items():
            for st in applicants[:self.remaining_seats[school]]:
                if st in self.offers:
                    self.offers[st].append(school)
                else:
                    self.offers[st] = [school]
        # 2. prijmi na nejlepsi offer a odstran z remaining_applicants
        for st, offs in self.offers.items():
            for sch in self.applications[st]:
                if sch in offs:
                    self.accepted[sch].add(st)
                    break
        self.remaining_applicants = {
            for sch, apps
        # 3. aktualizuj zbyvajici volna mista
        

    def has_finished(self) -> bool:
        not_finished = False
        for school, applicants in self.remaining_applicants.items():
            vacant = self.remaining_seats[school]
            not_finished = not_finished or bool(applicants[:vacant])
        return not not_finished

    def evaluate(self) -> Allocation:
        self.log_start()
        while not self.has_finished():
            self.step()
            self.log()
        ...
