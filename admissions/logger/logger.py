from typing import Dict
from admissions.domain import AdmissionData, Allocation


class Logger:
    """An interface for logging."""

    def __init__(self):
        self._name = ""

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    def log_start(self, admisison: AdmissionData):
        ...

    def log_step(self, data: Dict):
        ...

    def log_end(self, allocation: Allocation):
        ...
