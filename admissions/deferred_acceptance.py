from .domain import Admission
from .mechanism import Mechanism


class DeferredAcceptance(Mechanism):
    """
    Algoritmus:
        1. Každá škola posoudí všechny žaky, kteří si ji vybrali jako první, a těm
           s nejvyšší prioritou dle své kapacity nabídne podmíněné přijetí.
        2. U žáků, kteří nejsou podmíněně přijati, se pokračuje podle pořadí škol
           na přihláškách k další uvedené škole. Zde jsou tito žáci posouzeni společně
           se všemi dříve přijatými žáky a škola z nich opět vybere ty,
           které podmíněně přijme. Dle své kapacity může odmítnout i některé
           z již podmíněně přijatých žáků.
        3. Opakuje se bod 2, dokud nejsou všichni žáci podmíněně přijati nebo
           dokud nejsou zcela posouzené přihlášky všech nepřijatých žáků.
        4. Všichni podmíněně přijatí žáci jsou na tyto školy zapsáni.

    DA je nazývaný také student-optimal stable mechanism.
    """

    def __init__(self, data: Admission, verbose: bool = False):
        super().__init__(data, verbose=verbose)
        self.rejected = set()  # set of fully rejected students
        self.accepted = {s: set() for s in self.schools}  # conditional acceptance
        self.curr_positions = {s: 0 for s in self.students}
        self.vacant_seats = {k: v for k, v in self.seats.items()}
        # logging stuff
        self.num_steps = 0
        self.last_to_compare = {}
        self.last_positions = {}

    def log(self):
        if self.verbose:
            print(f"===  STEP = {self.num_steps}  ===")
            print(f"Position on applications: {self.last_positions}")
            print(f"Students to compare: {self.last_to_compare}")
            print(f"Accepted: {self.accepted}")
            print()

    def step(self):
        to_compare = {k: v for k, v in self.accepted.items()}
        # select students applying to a given school in this step
        for st, app in self.applications.items():
            curr_position = self.curr_positions[st]
            if curr_position < len(app):  # any school left on application
                to_compare[app[curr_position]].add(st)
        self.last_positions = {k: v for k, v in self.curr_positions.items()}
        self.last_to_compare = {}
        # and now...
        for sch, res in self.exams.items():
            num_seats = self.seats[sch]
            curr_students = to_compare[sch]
            curr_result = [st for st in res if st in curr_students]
            self.accepted[sch] = set(curr_result[:num_seats])
            for st in curr_result[num_seats:]:
                # move the curr_position for not-acepted students
                self.curr_positions[st] += 1

    def has_finished(self):
        # either all students accepted or no school left on not accepted
        # student's applications
        all_accepted = {st for x in self.accepted.values() for st in x}
        not_accepted = self.students - all_accepted
        has_finished = True
        for st in not_accepted:
            has_finished = has_finished and self.curr_positions[st] >= len(
                self.applications[st]
            )
        return has_finished

    def evaluate(self):
        self.log_start()
        while not self.has_finished():
            self.step()
            self.num_steps += 1
            self.log()
        # create final allocation and return
        all_accepted = {st for x in self.accepted.values() for st in x}
        rejected = self.students - all_accepted
        self.allocation = Allocation(matched=self.accepted, unmatched=rejected)
        self.log_end()
        return self.allocation
