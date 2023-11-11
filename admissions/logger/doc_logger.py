from typing import Mapping
from .logger import Logger
from ..domain import AdmissionData, Allocation
from .. import reportree as rt


class DocLogger(Logger):
    """
    Text Doc logger class:
        - create a simple rt.Doc and output the text there
        - so it is easy to construct full HTML report afterwards
    """

    _header = "h3"
    _subheader = "h4"

    def __init__(self, *args, **kwargs):
        super().__init__()
        self._num_steps = 0
        self.doc = rt.Doc(*args, **kwargs)

    def pretty_dict(self, data: Mapping):
        """Pomocná třída pro hezčí výpis dictionaries."""
        with self.doc.tag("ul"):
            for k, v in data.items():
                with self.doc.tag("li"):
                    self.doc.line("b", f"{k}: ")
                    self.doc.text(f"{v}\n")

    def log_start(self, admission_data: AdmissionData):
        self.doc.line(self._header, f"ADMISSION DATA")
        self.doc.line(self._subheader, "Students' applications")
        self.pretty_dict(admission_data.applications)

        self.doc.line(self._subheader, "School capacities")
        self.pretty_dict(admission_data.seats)

        self.doc.line(self._subheader, "School results")
        self.pretty_dict(admission_data.exams)

    def log_step(self, data: Mapping):
        self._num_steps += 1
        self.doc.line(self._header, f"STEP {self._num_steps}")
        self.pretty_dict(data)

    def log_end(self, allocation: Allocation):
        self.doc.line(self._header, "RESULTS")
        self.doc.line("div", f"Num steps: {self._num_steps}")
        self.doc.line(self._subheader, "Accepted")
        self.pretty_dict(allocation.accepted)
        self.doc.line(self._subheader, "Rejected")
        with self.doc.tag("ul"):
            self.doc.line("li", str(allocation.rejected))
