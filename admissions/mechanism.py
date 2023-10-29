from abc import ABC, abstractmethod
from types import Admission, SchoolId, StudentId


class Mechanism(ABC):
    def __init__(data: Admission) -> Allocation:
        ...


    @abstractmethod
    def evaluate(data: Admission) -> Allocation:
        raise NotImplementedError


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
    def evaluate(data: Admission):
        ...

