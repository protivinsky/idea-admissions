from copy import deepcopy
from typing import Any, Dict
from .domain import AdmissionData, Allocation
from .mechanism import Mechanism
from .logger import Logger


class DeferredAcceptance(Mechanism):
    """
    Mechanismus odloženého přijetí
    ------------------------------

    Také nazývaný **stabilní mechanismus optimální pro žáky**.

    *Deferred Acceptance mechanism (DA) / Student-optimal stable mechanism (SOSM)*

    **Algoritmus**

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

    DA je nazývaný také **student-optimal stable mechanism**, protože je nejlepším mechanismem
    pro studenty mezi všemi stabilními mechanismy (tedy bez opodstatněné závisti).
    """

    def __init__(self, data: AdmissionData, logger: Logger = Logger()):
        super().__init__(data, logger=logger)
        self.rejected = set()  # set of fully rejected students
        self.accepted = {s: set() for s in self.schools}  # conditional acceptance
        self.curr_positions = {s: 0 for s in self.students}
        self.vacant_seats = {k: v for k, v in self.seats.items()}

    def is_done(self):
        # either all students accepted or no school left on not accepted
        # student's applications
        all_accepted = {st for x in self.accepted.values() for st in x}
        not_accepted = self.students - all_accepted
        is_done = True
        for st in not_accepted:
            is_done = is_done and self.curr_positions[st] >= len(self.applications[st])
        return is_done

    def step(self) -> Dict[str, Any]:
        to_compare = {k: v for k, v in self.accepted.items()}
        # select students applying to a given school in this step
        for st, app in self.applications.items():
            curr_position = self.curr_positions[st]
            if curr_position < len(app):  # any school left on application
                to_compare[app[curr_position]].add(st)
        last_positions = {k: v for k, v in self.curr_positions.items()}
        # and now...
        for sch, res in self.exams.items():
            num_seats = self.seats[sch]
            curr_students = to_compare[sch]
            curr_result = [st for st in res if st in curr_students]
            self.accepted[sch] = set(curr_result[:num_seats])
            for st in curr_result[num_seats:]:
                # move the curr_position for not-acepted students
                self.curr_positions[st] += 1
        return deepcopy(
            {
                "__name__": self.__class__.__name__,
                "Position on applications": last_positions,
                "Students to compare": to_compare,
                "Accepted": self.accepted,
            }
        )

    def allocate(self) -> Allocation:
        accepted = {sch: frozenset(sts) for sch, sts in self.accepted.items()}
        all_accepted = {st for sts in self.accepted.values() for st in sts}
        rejected = self.students - all_accepted
        return Allocation(accepted=accepted, rejected=frozenset(rejected))
