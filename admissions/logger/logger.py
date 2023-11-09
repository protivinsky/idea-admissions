from abc import ABC, abstractmethod
from typing import Dict
from admissions.domain import Admission, Allocation


class Logger(ABC):
    """An interface for logging."""

    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def log_start(self, admission: Admission):
        raise NotImplementedError

    @abstractmethod
    def log_step(self, data: Dict):
        raise NotImplementedError

    @abstractmethod
    def log_end(self, allocation: Allocation):
        raise NotImplementedError
