from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple, Mapping, FrozenSet, Union

StudentId = Union[int, str]
SchoolId = Union[int, str]


@dataclass
class AdmissionData:
    applications: Mapping[StudentId, Tuple[SchoolId, ...]]
    exams: Mapping[SchoolId, Tuple[StudentId, ...]]
    seats: Mapping[SchoolId, int]

    def rename_schools(
        self, school_names: Mapping[SchoolId, SchoolId]
    ) -> AdmissionData:
        new_applications = {
            st: tuple(school_names[sch] for sch in schs)
            for st, schs in self.applications.items()
        }
        new_exams = {
            school_names[sch]: tuple(st for st in sts)
            for sch, sts in self.exams.items()
        }
        new_seats = {school_names[sch]: n for sch, n in self.seats.items()}
        return AdmissionData(
            applications=new_applications, exams=new_exams, seats=new_seats
        )

    def rename_students(
        self, student_names: Mapping[StudentId, StudentId]
    ) -> AdmissionData:
        new_applications = {
            student_names[st]: tuple(sch for sch in schs)
            for st, schs in self.applications.items()
        }
        new_exams = {
            sch: tuple(student_names[st] for st in sts)
            for sch, sts in self.exams.items()
        }
        new_seats = {sch: n for sch, n in self.seats.items()}
        return AdmissionData(
            applications=new_applications, exams=new_exams, seats=new_seats
        )

    def rename(
        self,
        student_names: Mapping[StudentId, StudentId],
        school_names: Mapping[SchoolId, SchoolId],
    ) -> AdmissionData:
        return self.rename_students(student_names).rename_schools(school_names)


@dataclass
class Allocation:
    accepted: Mapping[SchoolId, FrozenSet[StudentId]]
    rejected: FrozenSet[StudentId]

    def rename_schools(self, school_names: Mapping[SchoolId, SchoolId]) -> Allocation:
        new_accepted = {school_names[sch]: sts for sch, sts in self.accepted.items()}
        return Allocation(accepted=new_accepted, rejected=self.rejected)

    def rename_students(
        self, student_names: Mapping[StudentId, StudentId]
    ) -> Allocation:
        new_accepted = {
            sch: frozenset((student_names[st] for st in sts))
            for sch, sts in self.accepted.items()
        }
        new_rejected = frozenset({student_names[st] for st in self.rejected})
        return Allocation(accepted=new_accepted, rejected=frozenset(new_rejected))

    def rename(
        self,
        student_names: Mapping[StudentId, StudentId],
        school_names: Mapping[SchoolId, SchoolId],
    ) -> Allocation:
        return self.rename_students(student_names).rename_schools(school_names)
