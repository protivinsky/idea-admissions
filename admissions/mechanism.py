from abc import ABC, abstractmethod
from types import Admission, Allocation


class Mechanism(ABC):
    def __init__(self, data: Admission) -> Allocation:
        self.applications = data.applications
        self.exams = data.exams
        self.seats = data.seats
        self.school_names = data.school_names
        self.student_names = data.student_names

    @abstractmethod
    def evaluate(self) -> Allocation:
        raise NotImplementedError

    def validate_data(self):
        """
        Do some basic sanity checks on input data.
        """
        ...


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
    """
    def __init__(self, data: Admission):
        super().__init__(data)
        self.schools = set(self.seats.keys())
        self.students = set(self.applications.keys())
        self.rejected = {}  # set of fully rejected students
        self.accepted = {s: {} for s in self.schools}  # conditional acceptance
        self.curr_positions = {s: 0 for s in self.students}
        self.vacant_seats = {k: v for k, v in self.seats.items()}

    def step(self):
        to_compare = {k: v for k, v in self.accepted.items()}
        # select students applying to a given school in this step
        for st, app in self.applications:
            curr_position = self.app_positions[st]
            if curr_position < len(app):  # any school left on application
                to_compare[app[curr_position]].add(st)
        # and now...
        for sch, res in self.exams.items():
            num_seats = self.seats[sch]
            curr_students = to_compare[sch]
            curr_result = [st for st in res if st in curr_students]
            self.accepted[sch] = set(curr_result[:num_seats])
            for st in curr_result[num_seats:]
                # move the curr_position for not-acepted students
                self.curr_positions[st] += 1
    
    def has_finished(self):
        # either all students accepted or no school left on not accepted 
        # student's applications
        all_accepted = {st for x in self.accepted.values for st in x} 
        not_accepted = self.students - all_accepted
        has_finished = True
        for st in not_accepted:
            has_finished = (has_finished and 
                            self.curr_positions >= len(self.applications[st]))
        return has_finished

    def evaluate(self):
        while not has_finished():
            step()
        # create final allocation and return
        all_accepted = {st for x in self.accepted.values for st in x} 
        rejected = self.students - all_accepted
        return Allocation(matched=self.accepted, unmatched=rejected)
        

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
    """
    def __init__(self, data: Admission):
        super().__init__(data)

    def evaluate(self):
        ...

    
    




