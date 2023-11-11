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

        doc.line(self._subheader, "Studentské přihlášky")
        with doc.tag("table", klass="admission-table"):
            with doc.tag("tr"):
                for t in ["", "1. škola", "2. škola", "3. škola"]:
                    doc.line("th", t)
            for st, schs in admission_data.applications.items():
                with doc.tag("tr"):
                    with doc.tag("th", klass="app-student"):
                        doc.line("i", "", klass="bi bi-person-fill")
                        doc.text(f"  {st}")
                    for sch in schs:
                        doc.line("td", str(sch))

        schools = list(admission_data.exams.keys())
        max_exam_len = max([len(ex) for ex in admission_data.exams.values()])

        doc.line(self._subheader, "Výsledky školních zkoušek")
        with doc.tag("table", klass="admission-table"):
            with doc.tag("tr"):
                doc.line("th", "")
                for sch in schools:
                    with doc.tag("th", klass="exam-school"):
                        doc.line("i", "", klass="bi bi-house-fill")
                        doc.text(f"  {sch}")
            for i in range(max_exam_len):
                with doc.tag("tr"):
                    doc.line("td", f"{i + 1}.")
                    for sch in schools:
                        st = admission_data.exams[sch][i]
                        with doc.tag("td", klass="exam-student"):
                            doc.line("i", "", klass="bi bi-person-fill")
                            doc.text(f"  {st}")

    def log_step(self, data: Mapping):
        ...

    def log_end(self, allocation: Allocation):
        doc = self.doc
        doc.line(self._header, "Výsledek přijímaček")

        schools = sorted(list(allocation.accepted.keys()))

        # accepted
        doc.line(self._subheader, "Přijatí žáci")
        with doc.tag("ul", klass="admission-allocation"):
            for sch in schools:
                sts = allocation.accepted[sch]
                with doc.tag("li"):
                    doc.line("i", "", klass="bi bi-house-fill")
                    doc.line("b", f"  {sch}")
                    doc.line("i", "", klass="bi bi-arrow-left")
                    doc.line("i", "", klass="bi bi-person-fill")
                    st_text = "( " + ", ".join((f"  {st}" for st in sts)) + " )"
                    doc.text(st_text)

        # rejected
        if allocation.rejected:
            doc.line(self._subheader, "Nepřijatí žáci")
            with doc.tag("ul", klass="admission-allocation"):
                for st in allocation.rejected:
                    with doc.tag("li"):
                        doc.line("i", "", klass="bi bi-person-fill")
                        doc.text(str(st))
