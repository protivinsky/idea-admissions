from abc import ABC, abstractmethod
from typing import Set, Tuple
from .domain import Admission, Allocation, SchoolId, StudentId


class Mechanism(ABC):
    def __init__(self, data: Admission, verbose: bool = False) -> Allocation:
        self.applications = data.applications
        self.exams = data.exams
        self.seats = data.seats
        self.school_names = data.school_names
        self.student_names = data.student_names
        self.schools = set(self.seats.keys())
        self.students = set(self.applications.keys())
        self.verbose = verbose
        self.allocation = None

    @abstractmethod
    def evaluate(self) -> Allocation:
        raise NotImplementedError

    def validate_data(self):
        """
        Do some basic sanity checks on input data.
        """
        ...

    def log_start(self):
        if self.verbose:
            print(f'===  {self.__class__.__name__}  ===')
            print(f'Students\' applications: {self.applications}')
            print(f'School capacities: {self.seats}')
            print(f'School results: {self.exams}')
            print()

    def log_end(self):
        if self.verbose:
            print(f'===  RESULTS  ===')
            print(f'Accepted: {self.allocation.matched}')
            print(f'Rejected: {self.allocation.unmatched}')
            print()


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
            print(f'===  STEP = {self.num_steps}  ===')
            print(f'Position on applications: {self.last_positions}')
            print(f'Students to compare: {self.last_to_compare}')
            print(f'Accepted: {self.accepted}')
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
            has_finished = (has_finished and self.curr_positions[st]
                            >= len(self.applications[st]))
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
    def __init__(self, data: Admission, verbose: bool = False):
        super().__init__(data, verbose=verbose)
        self.applicants = {k: list(v) for k, v in self.exams.items()}
        self.cutoffs = {k: v for k, v in self.seats.items()}
        self.accepted = {s: set() for s in self.schools}
        self.max_school_rank = max(
                [len(app) for app in self.applications.values()])
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
                for st in apps[:self.cutoffs[sch]]:
                    # check if we have a new match
                    if st not in accepted and self.applications[st][i] == sch:
                        best_match.add((st, sch))
                        best_rank = i
            if best_match:
                break
        return best_rank, best_match

    def log(self):
        if self.verbose:
            print(f'===  STEP = {self.num_steps}  ===')
            print(f'Applicants: {self.applicants}')
            print(f'Accepted: {self.accepted}')
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
        for (st, sch) in best_match:
            self.accepted[sch].add(st)
            for other_sch in self.applications[st][best_rank + 1:]:
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
        self.allocation = Allocation(matched=self.accepted,
                                     unmatched=self.rejected())
        self.log_end()
        return self.allocation
    


