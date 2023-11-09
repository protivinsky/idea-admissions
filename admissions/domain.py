from dataclasses import dataclass
from typing import NewType, Tuple, Mapping, Optional, FrozenSet


StudentId = NewType("StudentId", int | str)
SchoolId = NewType("SchoolId", int | str)


@dataclass
class AdmissionData:
    applications: Mapping[StudentId, Tuple[SchoolId]]
    exams: Mapping[SchoolId, Tuple[StudentId]]
    seats: Mapping[SchoolId, int]


@dataclass
class Allocation:
    accepted: Mapping[SchoolId, FrozenSet[StudentId]]
    rejected: FrozenSet[StudentId]
