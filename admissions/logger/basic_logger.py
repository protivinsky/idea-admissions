from typing import Dict
from .logger import Logger
from ..domain import AdmissionData, Allocation


class BasicLogger(Logger):
    """
    Basic logger class:
        - text output of input admisison data, on every step and final allocation at the end
        - knows how to print dictionaries
    """

    def print_dict(self, d: Dict):
        """Pomocná třída pro hezčí výpis dictionaries."""
        return "{\n" + "\n".join([f"    {k}: {v}" for k, v in d.items()]) + "\n}\n"

    def log_start(self, admission_data: AdmissionData):
        print(f"===  {self.name}  ===")
        print(f"Students' applications: {self.print_dict(admission_data.applications)}")
        print(f"School capacities: {self.print_dict(admission_data.seats)}")
        print(f"School results: {self.print_dict(admission_data.exams)}")
        print()

    def log_end(self, allocation: Allocation):
        print(f"===  RESULTS  ===")
        print(f"Accepted: {self.print_dict(allocation.accepted)}")
        print(f"Rejected: {allocation.rejected}")
        print()
