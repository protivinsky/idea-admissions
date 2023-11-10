from typing import Dict, Any
from .domain import AdmissionData, Allocation
from .mechanism import Mechanism
from .logger import Logger


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

    def __init__(self, data: AdmissionData, logger: Logger = Logger()):
        super().__init__(data, logger=logger)
        self.applicants = {k: list(v) for k, v in self.exams.items()}
        self.cutoffs = {k: v for k, v in self.seats.items()}
        self.accepted = {s: set() for s in self.schools}
        self.max_school_rank = max([len(app) for app in self.applications.values()])
        self.current_best_rank = -1
        self.current_best_match = set()

    def find_best_match(self):
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
                        print(f"adding {st} @ {sch} to best match")
                        best_match.add((st, sch))
                        best_rank = i
            if best_match:
                break
        self.current_best_match = best_match
        self.current_best_rank = best_rank

    def is_done(self) -> bool:
        self.find_best_match()
        return not bool(self.current_best_match)

    def step(self) -> Dict[str, Any]:
        # -> add matched students to accepted lists
        # -> and remove them from unwanted schools
        for st, sch in self.current_best_match:
            self.accepted[sch].add(st)
            for other_sch in self.applications[st][self.current_best_rank + 1 :]:
                # remove the students from applications and accepted
                if st in self.applicants[other_sch]:
                    self.applicants[other_sch].remove(st)
                if st in self.accepted[other_sch]:
                    self.accepted[other_sch].remove(st)
        return {
            "Current best match": self.current_best_match,
            "Current best rank": self.current_best_rank,
            "Applicants": self.applicants,
            "Accepted": self.accepted,
        }

    def allocate(self) -> Allocation:
        accepted = {sch: frozenset(sts) for sch, sts in self.accepted.items()}
        all_accepted = {st for sts in self.accepted.values() for st in sts}
        rejected = self.students - all_accepted
        return Allocation(accepted=accepted, rejected=frozenset(rejected))
