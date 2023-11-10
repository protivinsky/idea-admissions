from typing import Dict, Any
from .domain import AdmissionData, Allocation
from .mechanism import Mechanism
from .logger import Logger


class SchoolOptimalSM(Mechanism):
    """
    School-optimal stable mechanism
    -------------------------------

    Cermat-proposed mechanism is equivalent to school-optimal stable mechanism.
    That is the stable mechanism that would be strictly preferred by schools.
    Students can achieve better outcome under student-optimal stable mechanism
    which is the deferred acceptance mechanism.

    Algoritmus:
        1. Podle výsledků zkoušky a vlastní kapacity každá škola stanoví,
           kteří žáci mají nárok na přijetí.
        2. Žáci s nárokem na přijetí jsou podmíněně přijati (pokud se následně nerozhodnou
           pro preferovanější školu) a z ostatních škol nad čarou jsou vyškrtnuti.
        3. Tím se na školách uvolní nová místa a přijímací hranici se posunou
           níže.
        4. Opakuje se od bodu 1, dokud zbývají žáci bez podmíněného přijetí a je možné
           pokračovat. Pokud v dalších kolech je žákům nabídnuta více preferovaná
           škola, mohou své rozhodnutí změnit.
    """

    def __init__(self, data: AdmissionData, logger: Logger = Logger()):
        super().__init__(data, logger=logger)
        self.accepted = {s: set() for s in self.schools}

    def is_done(self) -> bool:
        return True

    def step(self) -> Dict[str, Any]:
        ...

    def allocate(self) -> Allocation:
        accepted = {sch: frozenset(sts) for sch, sts in self.accepted.items()}
        all_accepted = {st for sts in self.accepted.values() for st in sts}
        rejected = self.students - all_accepted
        return Allocation(accepted=accepted, rejected=frozenset(rejected))
