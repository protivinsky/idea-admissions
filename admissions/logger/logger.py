from abc import ABC, abstractmethod
from typing import Dict
from admissions.domain import AdmissionData, Allocation


class Logger(ABC):
    """An interface for logging."""

    def __init__(self):
        self._name = ""

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @abstractmethod
    def log_start(self, admisison: AdmissionData):
        raise NotImplementedError

    @abstractmethod
    def log_step(self, data: Dict):
        raise NotImplementedError

    @abstractmethod
    def log_end(self, allocation: Allocation):
        raise NotImplementedError
