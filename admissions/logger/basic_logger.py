from typing import Mapping
from .logger import Logger
from ..domain import AdmissionData, Allocation


class BasicLogger(Logger):
    """
    Basic logger class:
        - text output of input admisison data, on every step and final allocation at the end
        - knows how to print dictionaries
    """

    def __init__(self):
        super().__init__()
        self._num_steps = 0

    def pretty_dict(self, data: Mapping):
        """Pomocná třída pro hezčí výpis dictionaries."""
        return "{\n" + "\n".join([f"    {k}: {v}" for k, v in data.items()]) + "\n}\n"

    def log_start(self, admission_data: AdmissionData):
        print(f"===  {self.name}  ===")
        print(
            f"Students' applications: {self.pretty_dict(admission_data.applications)}"
        )
        print(f"School capacities: {self.pretty_dict(admission_data.seats)}")
        print(f"School results: {self.pretty_dict(admission_data.exams)}")
        print()

    def log_step(self, data: Mapping):
        self._num_steps += 1
        print(f"===  STEP {self._num_steps}  ===")
        print(self.pretty_dict(data))
        print()

    def log_end(self, allocation: Allocation):
        print("===  RESULTS  ===")
        print(f"Accepted: {self.pretty_dict(allocation.accepted)}")
        print(f"Rejected: {allocation.rejected}")
        print()
