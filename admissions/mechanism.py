from abc import ABC, abstractmethod
from typing import Set, Tuple
from .domain import Admission, Allocation, SchoolId, StudentId


class Mechanism(ABC):
    def __init__(self, data: Admission, verbose: bool = False):
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
            print(f"===  {self.__class__.__name__}  ===")
            print(f"Students' applications: {self.applications}")
            print(f"School capacities: {self.seats}")
            print(f"School results: {self.exams}")
            print()

    def log_end(self):
        if self.verbose:
            print(f"===  RESULTS  ===")
            print(f"Accepted: {self.allocation.matched}")
            print(f"Rejected: {self.allocation.unmatched}")
            print()
