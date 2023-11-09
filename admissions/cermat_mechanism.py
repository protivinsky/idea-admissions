from typing import Set, Tuple
from .domain import AdmissionData, Allocation, SchoolId, StudentId
from .mechanism import Mechanism


class CermatMechanism(Mechanism):
    """
    Algoritmus:
        1. Podle výsledků zkoušky a vlastní kapacity každá škola stanoví,
           kteří žáci mají nárok na přijetí.
        2. Mezi žáky s nárokem na přijetí se vyberou ti, kteří tuto školu
           uvedli na prvním místě. Pokud se žádní
           takoví žáci nevyskytují, vyberou se žáci přijatí na školu na
           druhém místě (pokud by se ani takoví nevyskytovali, lze analogicky
           pokračovat k dalším v pořadí).
        3. Tito žáci jsou přijatí na danou školu a jsou vyškrnuti ze seznamů
           všech škol, které uvedli na horší pozici v přihláškách. Mohou tak
           být vyškrnuti i ze školy, na kterou byli dříve přijati.
        4. Tím se na školách uvolní nová místa a přijímací hranici se posunou
           níže.
        5. Opakuje se od bodu 2, dokud zbývají nepřijatí žáci a je možné
           pokračovat.

    Tento mechanismus je ekvivalentní ke school-optimal stable mechanism.
    Vede tedy také ke stabilnímu párování, které je však optimální z pohledu
    škol, nikoli studentů.
    """

    def __init__(self, data: AdmissionData, verbose: bool = False):
        super().__init__(data, verbose=verbose)
        self.applicants = {k: list(v) for k, v in self.exams.items()}
        self.cutoffs = {k: v for k, v in self.seats.items()}
        self.accepted = {s: set() for s in self.schools}
        self.max_school_rank = max([len(app) for app in self.applications.values()])
        # the below is mainly for logging
        self.num_steps = 0
        self.last_best_match = set()
        self.last_best_rank = -1

    def rejected(self):
        all_accepted = {st for x in self.accepted.values() for st in x}
        rejected = self.students - all_accepted
        return rejected

    def find_best_match(self) -> Tuple[int, Set[Tuple[StudentId, SchoolId]]]:
        # returns the best rank and set of best-match students
        best_match = set()
        best_rank = -1
        # consider all possible ranks up to the max application length
        for i in range(self.max_school_rank):
            # go through schools and try to find given rank match
            for sch, apps in self.applicants.items():
                accepted = self.accepted[sch]
                # for applicants above cutoff, check the rank of the match
                for st in apps[: self.cutoffs[sch]]:
                    # check if we have a new match
                    if st not in accepted and self.applications[st][i] == sch:
                        best_match.add((st, sch))
                        best_rank = i
            if best_match:
                break
        return best_rank, best_match

    def log(self):
        if self.verbose:
            print(f"===  STEP = {self.num_steps}  ===")
            print(f"Applicants: {self.applicants}")
            print(f"Accepted: {self.accepted}")
            print()

    def step(self) -> bool:
        # If returns True, some students were allocated and we should continue.
        # search for the best rank
        best_rank, best_match = self.find_best_match()
        self.last_best_rank = best_rank
        self.last_best_match = best_match
        # if there are no students with best match, return and end
        if not best_match:
            return False
        self.num_steps += 1
        # -> add matched students to accepted lists
        # -> and remove them from unwanted schools
        for st, sch in best_match:
            self.accepted[sch].add(st)
            for other_sch in self.applications[st][best_rank + 1 :]:
                # remove the students from applications and accepted
                if st in self.applicants[other_sch]:
                    self.applicants[other_sch].remove(st)
                if st in self.accepted[other_sch]:
                    self.accepted[other_sch].remove(st)
        self.log()
        return True

    def evaluate(self):
        self.log_start()
        while self.step():
            pass
        self.allocation = Allocation(accepted=self.accepted, rejected=self.rejected())
        self.log_end()
        return self.allocation
