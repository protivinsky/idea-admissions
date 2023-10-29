from dataclasses import dataclass
from typing import NewType, Tuple, Mapping, Optional, FrozenSet


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


@dataclass
class Allocation:
    matched: Mapping[SchoolId, FrozenSet[StudentId]]
    unmatched: FrozenSet[StudentId]
