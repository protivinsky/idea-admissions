from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import NewType, Tuple, Mapping, FrozenSet, Set, Dict


# Pomocné typy pro type hints.
StudentId = NewType("StudentId", int | str)
SchoolId = NewType("SchoolId", int | str)


@dataclass
class Admission:
    """
    Vstupní data:
        applications: Přihlášky studentů; pro každého studenta určitý počet
            seřazených škol dle preferencí.
        exams: Pro každou školu máme pořadí všech žáků, kteří se na ni hlásí.
        seats: Kapacita jednotlivých škol.
    """

    applications: Mapping[StudentId, Tuple[SchoolId]]
    exams: Mapping[SchoolId, Tuple[StudentId]]
    seats: Mapping[SchoolId, int]


@dataclass
class Allocation:
    """
    Výsledné přiřazení žáků do škol:
        matched: Seznam studentů pro jednotlivé školy (tedy již automaticky
            zapsaní).
        unmatched: Zcela odmítnutí studenti, kteří pokračují do druhého kola.
    """

    matched: Mapping[SchoolId, FrozenSet[StudentId]]
    unmatched: FrozenSet[StudentId]


def print_dict(d: Dict):
    """Pomocná třída pro hezčí výpis dictionaries."""
    return "{\n" + "\n".join([f"    {k}: {v}" for k, v in d.items()]) + "\n}\n"


class Mechanism(ABC):
    """Abstract base class pro párovací mechanismus."""

    def __init__(self, data: Admission, verbose: bool = False) -> Allocation:
        self.applications = data.applications
        self.exams = data.exams
        self.seats = data.seats
        self.schools = set(self.seats.keys())
        self.students = set(self.applications.keys())
        self.verbose = verbose
        self.allocation = None

    @abstractmethod
    def evaluate(self) -> Allocation:
        raise NotImplementedError

    def log_start(self):
        if self.verbose:
            print(f"===  {self.__class__.__name__}  ===")
            print(f"Students' applications: {print_dict(self.applications)}")
            print(f"School capacities: {print_dict(self.seats)}")
            print(f"School results: {print_dict(self.exams)}")
            print()

    def log_end(self):
        if self.verbose:
            print(f"===  RESULTS  ===")
            print(f"Accepted: {print_dict(self.allocation.accepted)}")
            print(f"Rejected: {self.allocation.rejected}")
            print()


class DeferredAcceptance(Mechanism):
    """
    MECHANISMUS ODLOŽENÉHO PŘIJETÍ

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
        # accepted = seznam žáků, kteří jsou momentálně podmíněně přijati
        #   na danou školu
        self.accepted = {s: set() for s in self.schools}
        # curr_positions = aktuálně vyhodnocovaná pozice na přihláškách
        #   jednotlivých žáků
        self.curr_positions = {s: 0 for s in self.students}
        # logging stuff
        self.num_steps = 0
        self.last_to_compare = {}
        self.last_positions = {}

    def log(self):
        if self.verbose:
            print(f"===  STEP = {self.num_steps}  ===")
            print(f"Position on applications: {print_dict(self.last_positions)}")
            print(f"Students to compare: {print_dict(self.last_to_compare)}")
            print(f"Accepted: {print_dict(self.accepted)}")
            print()

    def step(self):
        """
        Hlavní krok celého algoritmu:
            - pro každou školu se vytvoří seznam žáků, kteří jsou momentálně
                společně posuzování: tvoři ho již dříve podmíněně
                přijatí žáci na danou školu a nepřijatí žáci, kteří mají
                tuto školu jako další na své přihlášce.
            - z těchto seznamů se vyberou nejúspěšnější žáci dle školní zkoušky
                (do naplnění kapacity), kteří dostávají podmíněné přijetí.
                Ostatní jsou odmítnuti a na jejich přihláškách se posouváme
                na další pozici.
        """
        to_compare = {k: v for k, v in self.accepted.items()}
        # select students applying to a given school in this step
        for st, app in self.applications.items():
            curr_position = self.curr_positions[st]
            if curr_position < len(app):  # any school left on application
                to_compare[app[curr_position]].add(st)
        self.last_positions = {k: v + 1 for k, v in self.curr_positions.items()}
        self.last_to_compare = {k: v for k, v in to_compare.items()}
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
        """
        Algoritmus končí, pokud nastane jedna ze dvou podmínek:
            - všichni žáci jsou přijati
            - u stále nepřijatých žáků již byly posouzeny všechny školy
                z jejich přihlášek
        Tedy v okamžiku, kdy každý žak je buď přijatý, nebo už byly posouzeny
        všechny školy z jeho přihlášky.
        """
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
        # Podmíněná přijetí jsou potvrzena a žáci mohou být zapsáni.
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
            print(f"Applicants: {print_dict(self.applicants)}")
            print(f"Accepted: {print_dict(self.accepted)}")
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
        self.allocation = Allocation(matched=self.accepted, unmatched=self.rejected())
        self.log_end()
        return self.allocation


# První modelová situace z přílohy naší studie.
example_1 = Admission(
    applications={
        1: ("A", "B", "C"),
        2: ("A", "B", "D"),
        3: ("A", "C", "D"),
        4: ("B", "C", "D"),
    },
    exams={
        "A": (1, 2, 3),
        "B": (1, 2, 4),
        "C": (1, 3, 4),
        "D": (2, 3, 4),
    },
    seats={k: 1 for k in "ABCD"},
)


# Druhá modelová situace ze studie.
example_2 = Admission(
    applications={
        1: ("A", "B", "C"),
        2: ("B", "A", "C"),
        3: ("A", "B", "C"),
    },
    exams={
        "A": (2, 1, 3),
        "B": (1, 2, 3),
        "C": (1, 2, 3),
    },
    seats={k: 1 for k in "ABC"},
)


# Příklad záměrně navržený tak, aby ilustroval rozdíl mezi mechanismem
# odloženého přijetí a cermat mechanismem.
example_3 = Admission(
    applications={
        1: ("A", "B", "C"),
        2: ("B", "C", "A"),
        3: ("C", "A", "B"),
    },
    exams={
        "A": (2, 3, 1),
        "B": (3, 1, 2),
        "C": (1, 2, 3),
    },
    seats={k: 1 for k in "ABC"},
)


# Tento příklad ilustruje situaci, kdy ve výsledku již není možné prohodit žáky
# pod čarou, neboť by tím došlo k vytvoření nespravedlnosti ve výsledku.
example_4 = Admission(
    applications={
        1: ("B", "A", "C"),
        2: ("A", "B", "C"),
        3: ("A", "B", "C"),
    },
    exams={
        "A": (1, 3, 2),
        "B": (2, 1, 3),
        "C": (2, 1, 3),
    },
    seats={k: 1 for k in "ABC"},
)


# Přiklad z videa.
example_cermat_school_names = {
    1: "Gymnázium Nymburk",
    2: "Lyceum Mělník",
    3: "SOŠ Smíchov",
}

example_cermat_student_list = [
    "Adam",
    "Bára",
    "Cecílie",
    "Dan",
    "Eda",
    "Filip",
    "Gustav",
    "Hanka",
    "Ivana",
    "Jana",
    "Katka",
    "Lenka",
    "Marek",
]
example_cermat_student_names = {s[0]: s for s in example_cermat_student_list}
example_cermat_exams = {
    1: tuple([s for s in "AIDMECJBLFHKG"]),
    2: tuple([s for s in "CGIAHMLKJEFDB"]),
    3: tuple([s for s in "IGBKCADMEHLJF"]),
}
example_cermat_applications = {
    "A": (2, 3, 1),
    "B": (2, 1, 3),
    "C": (3, 2, 1),
    "D": (2, 1, 3),
    "E": (2, 1, 3),
    "F": (1, 3, 2),
    "G": (1, 3, 2),
    "H": (1, 2, 3),
    "I": (3, 2, 1),
    "J": (2, 3, 1),
    "K": (2, 3, 1),
    "L": (1, 3, 2),
    "M": (3, 2, 1),
}

example_cermat_applications = {
    example_cermat_student_names[k]: tuple(
        (example_cermat_school_names[sch] for sch in v)
    )
    for k, v in example_cermat_applications.items()
}

example_cermat_exams = {
    example_cermat_school_names[k]: tuple(
        (example_cermat_student_names[st] for st in v)
    )
    for k, v in example_cermat_exams.items()
}

example_cermat_seats = {
    example_cermat_school_names[1]: 4,
    example_cermat_school_names[2]: 3,
    example_cermat_school_names[3]: 5,
}

example_cermat = Admission(
    applications=example_cermat_applications,
    exams=example_cermat_exams,
    seats=example_cermat_seats,
)


if __name__ == "__main__":
    print()
    print("===============================================")
    print()

    cm = CermatMechanism(example_cermat, verbose=True)
    cm.evaluate()

    print()
    print("===============================================")
    print()

    da = DeferredAcceptance(example_cermat, verbose=True)
    da.evaluate()

    print()
    print("===============================================")
    print()
