from typing import Mapping
from .logger import Logger
from ..domain import AdmissionData, Allocation
from .. import reportree as rt


class GraphicLogger(Logger):
    """
    Full graphic logger
    - can output generic classes - AdmissionData and AllocationData into nice tables
    - can be further extended to handle properly the step output of different mechanism
      with more fine-tuned output
    """

    _header = "h2"
    _subheader = "h3"

    def __init__(self, *args, **kwargs):
        super().__init__()
        self._num_steps = 0
        self.doc = rt.Doc(*args, **kwargs)

    def log_start(self, admission_data: AdmissionData):
        doc = self.doc
        doc.line(self._header, "Vstupní data")

        with doc.tag("table", klass="admission-table"):
            with doc.tag("tr"):
                doc.line("th", "Studentské přihlášky", colspan=4)
            with doc.tag("tr"):
                for t in ["", "1. škola", "2. škola", "3. škola"]:
                    doc.line("th", t)
            for st, schs in admission_data.applications.items():
                with doc.tag("tr"):
                    with doc.tag("th"):
                        doc.line("i", "", klass="bi bi-person-fill")
                        doc.text(f"  {st}")
                    for sch in schs:
                        doc.line("td", str(sch))

    def log_step(self, data: Mapping):
        ...

    def log_end(self, allocation: Allocation):
        ...
