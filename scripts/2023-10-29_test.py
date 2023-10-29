from dataclasses import dataclass
from typing import NewType, Dict, List, Tuple, Union, Mapping, Optional
from frozendict import frozendict


StudentId = NewType('StudentId', int | str)
SchoolId = NewType('SchoolId', int | str)


# Ideally, I would define all the types as immutable...
# Python is not much helpful here unless I use frozendict and likes.
@dataclass
class Admission:
    applications: Mapping[StudentId,Tuple[SchoolId]]
    results: Mapping[SchoolId, Tuple[StudentId]]
    seats: Mapping[SchoolId, int]
    school_names: Optional[Mapping[SchoolId, str]]
    student_names: Optional[Mapping[StudentId, str]]


# define the basic examples - from the report and from Cermat video

ex1 = Admission(
    applications = {
        1: ('A', 'B', 'C'),
        2: ('A', 'B', 'D'),
        3: ('A', 'C', 'D'),
        4: ('B', 'C', 'D'),
    },
    results = {k: (1, 2, 3, 4) for k in 'ABCD'},
    seats = {k: 1 for k in 'ABCD'},
)

ex2 = Admission(
    applications = {
        1: ('A', 'B', 'C'),
        2: ('B', 'A', 'C'),
        3: ('A', 'B', 'C'),
    },
    results = {
        'A': (2, 1, 3),
        'B': (1, 2, 3),
        'C': (1, 2, 3),
    },
    seats = {k: 1 for k in 'ABC'},
)


ex_cermat_school_names = {
    1: 'Gymnázium Nymburk',
    2: 'Lyceum Mělník',
    3: 'SOŠ Smíchov',
}

ex_cermat_student_list = ['Adam', 'Bára', 'Cecílie', 'Dan', 'Eda', 'Filip', 'Gustav',
    'Hanka', 'Ivana', 'Jana', 'Katka', 'Lenka', 'Marek']
ex_cermat_student_names = {s: s[0] for s in ex_cermat_student_list}
ex_cermat_results = {
    1: tuple([s for s in 'AIDMECJBLFHKG']),
    2: tuple([s for s in 'CGIAHMLKJEFDB']),
    3: tuple([s for s in 'IGBKCADMEHLJF']),
}
ex_cermat_applications = {
    'A': (2, 3, 1),
    'B': (2, 1, 3),
    'C': (3, 2, 1),
    'D': (2, 1, 3),
    'E': (2, 1, 3),
    'F': (1, 3, 2),
    'G': (1, 3, 2),
    'H': (1, 2, 3),
    'I': (3, 2, 1),
    'J': (2, 3, 1),
    'K': (2, 3, 1),
    'L': (1, 3, 2),
    'M': (3, 2, 1),
}


ex_cermat = Admission(
    applications = ex_cermat_applications,
    results = ex_cermat_results,
    seats = {1: 4, 2: 3, 3: 5},
    school_names = ex_cermat_school_names,
    student_names = ex_cermat_student_names,
)


ex2


for x in 'abcd':
    print(x)

[x for x in 'abcd']
{x: x for x in 'abcd'}




