from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from .domain import AdmissionData, Allocation
from .logger import Logger


class Mechanism(ABC):
    def __init__(self, admission_data: AdmissionData, logger: Logger = Logger()):
        self.validate_data(admission_data)
        self.admission_data = admission_data
        self.students = set(self.admission_data.applications.keys())
        self.schools = set(self.admission_data.exams.keys())
        self.logger = logger
        self.logger.name = self.__class__.__name__

    @property
    def applications(self):
        return self.admission_data.applications

    @property
    def exams(self):
        return self.admission_data.exams

    @property
    def seats(self):
        return self.admission_data.seats

    def validate_data(self, admission_data: AdmissionData):
        """
        Do some basic sanity checks on input data.
        """
        ...

    @abstractmethod
    def is_done(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def step(self) -> Dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def allocate(self) -> Allocation:
        raise NotImplementedError

    def evaluate(self) -> Allocation:
        self.logger.log_start(self.admission_data)
        while not self.is_done():
            logging_data = self.step()
            self.logger.log_step(logging_data)

        allocation = self.allocate()
        self.logger.log_end(allocation)
        return allocation
