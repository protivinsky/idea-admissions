from abc import ABC, abstractmethod
from typing import Optional
from .domain import AdmissionData, Allocation, SchoolId, StudentId
from logger.logger import Logger


class Mechanism(ABC):
    def __init__(self, admission_data: AdmissionData, logger: Optional[Logger] = None):
        self.validate_data(admission_data)
        self.admission_data = admission_data
        self.students = set(self.admission_data.applications.keys())
        self.schools = set(self.admission_data.exams.keys())
        if logger is not None:
            logger.name = self.__class__.__name__

    @abstractmethod
    def evaluate(self) -> Allocation:
        raise NotImplementedError

    def validate_data(self, admission_data: AdmissionData):
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
