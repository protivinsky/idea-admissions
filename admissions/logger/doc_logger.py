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

    def __init__(self, *args, **kwargs):
        super().__init__()
        self._num_steps = 0
        self.doc = rt.Doc(*args, **kwargs)

    def pretty_dict(self, data: Mapping):
        """Pomocná třída pro hezčí výpis dictionaries."""
        with self.doc.tag("ul"):
            for k, v in data.items():
                with self.doc.tag("li"):
                    self.doc.line("b", f"{k}:")
                    self.doc.text(f"{v}\n")

    def log_start(self, admission_data: AdmissionData):
        self.doc.line("h2", f"===  {self.name}  ===")
        self.doc.line("h3", "Students' applications")
        self.doc.line("pre", self.pretty_dict(admission_data.applications))

        self.doc.line("h3", "School capacities")
        self.doc.line("pre", self.pretty_dict(admission_data.seats))

        self.doc.line("h3", "School results")
        self.doc.line("pre", self.pretty_dict(admission_data.exams))
        self.doc.stag("br")

    def log_step(self, data: Mapping):
        self._num_steps += 1
        self.doc.line("h2", f"===  STEP {self._num_steps}  ===")
        self.doc.line("pre", self.pretty_dict(data))
        self.doc.stag("br")

    def log_end(self, allocation: Allocation):
        self.doc.line("h2", "===  RESULTS  ===")
        self.doc.line("div", f"Num steps: {self._num_steps}")
        self.doc.line("h3", "Accepted")
        self.doc.line("pre", self.pretty_dict(allocation.accepted))
        self.doc.line("h3", "Rejected")
        self.doc.line("pre", str(allocation.rejected))
        self.doc.stag("br")
