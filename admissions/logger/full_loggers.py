from os import waitid_result
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
    _subsubheader = "h4"

    def __init__(self, *args, **kwargs):
        super().__init__()
        self._num_steps = 0
        self.doc = rt.Doc(*args, **kwargs)
        self._step_data = []

    def log_start(self, admission_data: AdmissionData):
        self._admission_data = admission_data

    def log_step(self, data: Mapping):
        self._num_steps += 1
        self._step_data.append(data)

    def at_end_log_start(self, admission_data: AdmissionData):
        doc = self.doc

        accepted = self._allocation.accepted
        rejected = self._allocation.rejected

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
                        extra_klass = (
                            "green-black" if st in accepted[sch] else "red-black"
                        )
                        doc.line("td", str(sch), klass=extra_klass)

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
                        doc.stag("br")
                        doc.line(
                            "small",
                            f"Míst = {admission_data.seats[sch]}",
                            style="font-weight: normal;",
                        )
            for i in range(max_exam_len):
                with doc.tag("tr"):
                    doc.line("th", f"{i + 1}.")
                    for sch in schools:
                        st = admission_data.exams[sch][i]
                        extra_klass = (
                            "green-black" if st in accepted[sch] else "red-black"
                        )
                        with doc.tag("td", klass=f"exam-student {extra_klass}"):
                            doc.line("i", "", klass="bi bi-person-fill")
                            doc.text(f"  {st}")

    def at_end_log_step(self, data: Mapping):
        self._num_steps += 1
        if "__name__" not in data:
            return
        mech = data["__name__"]
        if mech == "CermatMechanism":
            self.log_step_cermat(data)
        elif mech == "SchoolOptimalSM":
            self.log_step_school_optimal_sm(data)
        elif mech == "NaiveMechanism":
            self.log_step_naive(data)
        elif mech == "DeferredAcceptance":
            self.log_step_da(data)
        else:
            self.doc.line("b", "Neznámý mechanismus")

    def log_end(self, allocation: Allocation):
        self._allocation = allocation
        doc = self.doc
        doc.line(self._header, "Výsledek přijímaček")

        schools = sorted(list(allocation.accepted.keys()))

        # accepted
        doc.line(self._subheader, "Přijatí žáci")

        with doc.tag("table", klass="admission-table"):
            for sch in schools:
                sts = allocation.accepted[sch]
                with doc.tag("tr"):
                    with doc.tag("td", klass="allocation"):
                        doc.line("i", "", klass="bi bi-house-fill")
                        doc.line("b", f"  {sch}")
                        doc.line(
                            "small",
                            f"[ Míst = {self._admission_data.seats[sch]} ]",
                            style="font-weight: normal;",
                        )
                    with doc.tag("td", klass="allocation green-black"):
                        doc.line("i", "", klass="bi bi-person-fill")
                        doc.text(", ".join((f"  {st}" for st in sorted(list(sts)))))

        if allocation.rejected:
            doc.line(self._subheader, "Nepřijatí žáci")
            with doc.tag("table", klass="admission-table"):
                with doc.tag("tr"):
                    with doc.tag("td", klass="allocation red-black"):
                        doc.line("i", "", klass="bi bi-person-fill")
                        doc.text(
                            ", ".join(
                                (f"  {st}" for st in sorted(list(allocation.rejected)))
                            )
                        )

        self._num_steps = 0
        self.at_end_log_start(self._admission_data)
        self.doc.line(self._header, "Průběh algoritmu")
        # self.at_end_before_steps()
        for step_data in self._step_data:
            self.at_end_log_step(step_data)

    def log_step_da(self, data: Mapping):
        doc = self.doc

        schools = list(self._admission_data.exams.keys())
        if not hasattr(self, "_prev_rejected"):
            self._prev_rejected = {sch: set() for sch in schools}
        max_exam_len = max([len(ex) for ex in self._admission_data.exams.values()])
        exams = self._admission_data.exams
        applications = self._admission_data.applications

        last_positions = data["Position on applications"]
        last_to_compare = data["Students to compare"]
        accepted = data["Accepted"]
        all_accepted = {st for sts in accepted.values() for st in sts}

        doc.line(self._subheader, f"Krok {self._num_steps}")

        doc.line(self._subheader, f"PODLE VÝSLEDKŮ ZKOUŠKY")
        doc.line(self._subsubheader, "NABÍDKY")
        with doc.tag("div"):
            doc.line("b", "PODLE VÝSLEDKŮ ZKOUŠKY")

        with doc.tag("table", klass="admission-table da-step-table"):
            with doc.tag("tr"):
                doc.line("th", "")
                for sch in schools:
                    with doc.tag("th", klass="exam-school"):
                        doc.line("i", "", klass="bi bi-house-fill")
                        doc.text(f"  {sch}")
                        doc.stag("br")
                        doc.line(
                            "small",
                            f"Míst = {self._admission_data.seats[sch]}",
                            style="font-weight: normal;",
                        )
            for i in range(max_exam_len):
                with doc.tag("tr"):
                    doc.line("th", f"{i + 1}.")
                    for sch in schools:
                        st = self._admission_data.exams[sch][i]
                        # offered / not-evaluated / last-offered / removed
                        if st in self._prev_rejected[sch]:
                            extra_klass = "red-red"
                        elif sch in last_to_compare and st in last_to_compare[sch]:
                            extra_klass = "yellow-yellow"
                        else:
                            extra_klass = "gray-gray"
                        # if j == last_positions[st]:
                        #     extra_klass += " right-border"
                        with doc.tag("td", klass=f"exam-student {extra_klass}"):
                            doc.line("i", "", klass="bi bi-person-fill")
                            doc.text(f"  {st}")

        with doc.tag("div"):
            doc.line("b", "PODLE PŘIHLÁŠEK")

        doc.line(self._subsubheader, "PŘIJATÉ A ODMÍTNUTÉ")

        with doc.tag("div"):
            doc.line("b", "PODLE VÝSLEDKŮ ZKOUŠKY")

        with doc.tag("table", klass="admission-table da-step-table"):
            with doc.tag("tr"):
                doc.line("th", "")
                for sch in schools:
                    with doc.tag("th", klass="exam-school"):
                        doc.line("i", "", klass="bi bi-house-fill")
                        doc.text(f"  {sch}")
                        doc.stag("br")
                        doc.line(
                            "small",
                            f"Míst = {self._admission_data.seats[sch]}",
                            style="font-weight: normal;",
                        )
            for i in range(max_exam_len):
                with doc.tag("tr"):
                    doc.line("th", f"{i + 1}.")
                    for sch in schools:
                        st = self._admission_data.exams[sch][i]
                        # accepted / removed / not-evaluated / last-offered
                        if (
                            sch in last_to_compare
                            and st in last_to_compare[sch]
                            and st not in accepted[sch]
                        ):
                            self._prev_rejected[sch].add(st)
                        if st in accepted[sch]:
                            extra_klass = "green-green"
                        elif st in self._prev_rejected[sch]:
                            extra_klass = "red-red"
                        elif st in all_accepted:
                            extra_klass = "gray-gray"
                        else:
                            extra_klass = ""
                        with doc.tag("td", klass=f"exam-student {extra_klass}"):
                            doc.line("i", "", klass="bi bi-person-fill")
                            doc.text(f"  {st}")

        with doc.tag("div"):
            doc.line("b", "PODLE PŘIHLÁŠEK")

    def log_step_school_optimal_sm(self, data: Mapping):
        """ """
        doc = self.doc

        schools = list(self._admission_data.exams.keys())
        # if not hasattr(self, "_prev_rejected"):
        #     self._prev_rejected = {sch: {} for sch in schools}
        max_exam_len = max([len(ex) for ex in self._admission_data.exams.values()])

        exams = self._admission_data.exams
        remaining_applicants = data["Remaining applicants"]
        offers = data["Offers"]
        accepted = data["Accepted"]

        doc.line(self._subheader, f"Krok {self._num_steps}")
        doc.line(self._subsubheader, "NABÍDKY")

        # what do I need here?
        # - how many are still below the line
        # - offers
        above_line = {
            sch: len(exams[sch]) - len(sts) for sch, sts in remaining_applicants.items()
        }

        with doc.tag("table", klass="admission-table school-optimal-step-table"):
            with doc.tag("tr"):
                doc.line("th", "")
                for sch in schools:
                    with doc.tag("th", klass="exam-school"):
                        doc.line("i", "", klass="bi bi-house-fill")
                        doc.text(f"  {sch}")
                        doc.stag("br")
                        doc.line(
                            "small",
                            f"Míst = {self._admission_data.seats[sch]}",
                            style="font-weight: normal;",
                        )
            for i in range(max_exam_len):
                with doc.tag("tr"):
                    doc.line("th", f"{i + 1}.")
                    for sch in schools:
                        st = self._admission_data.exams[sch][i]
                        # offered / not-evaluated / last-offered / removed
                        if i < above_line[sch]:
                            extra_klass = "offered" if sch in offers[st] else "removed"
                        else:
                            extra_klass = "not-evaluated"
                        if i == above_line[sch] - 1:
                            extra_klass += " last-offered"
                        with doc.tag("td", klass=f"exam-student {extra_klass}"):
                            doc.line("i", "", klass="bi bi-person-fill")
                            doc.text(f"  {st}")

        doc.line(self._subsubheader, "PŘIJATÉ A ODMÍTNUTÉ")

        with doc.tag("table", klass="admission-table school-optimal-step-table"):
            with doc.tag("tr"):
                doc.line("th", "")
                for sch in schools:
                    with doc.tag("th", klass="exam-school"):
                        doc.line("i", "", klass="bi bi-house-fill")
                        doc.text(f"  {sch}")
                        doc.stag("br")
                        doc.line(
                            "small",
                            f"Míst = {self._admission_data.seats[sch]}",
                            style="font-weight: normal;",
                        )
            for i in range(max_exam_len):
                with doc.tag("tr"):
                    doc.line("th", f"{i + 1}.")
                    for sch in schools:
                        st = self._admission_data.exams[sch][i]
                        # accepted / removed / not-evaluated / last-offered
                        if i < above_line[sch]:
                            extra_klass = (
                                "accepted" if st in accepted[sch] else "removed"
                            )
                        else:
                            extra_klass = "not-evaluated"
                        if i == above_line[sch] - 1:
                            extra_klass += " last-offered"
                        with doc.tag("td", klass=f"exam-student {extra_klass}"):
                            doc.line("i", "", klass="bi bi-person-fill")
                            doc.text(f"  {st}")

    def log_step_naive(self, data: Mapping):
        doc = self.doc

        schools = list(self._admission_data.exams.keys())
        if not hasattr(self, "_prev_accepted"):
            self._prev_accepted = {sch: set() for sch in schools}
        if not hasattr(self, "_prev_removed"):
            self._prev_removed = {sch: set() for sch in schools}

        offers = data["Current offers"]
        accepted = data["Accepted"]
        remaining_seats = data["Remaining seats"]
        all_accepted = {st for sts in accepted.values() for st in sts}
        max_exam_len = max([len(ex) for ex in self._admission_data.exams.values()])
        exams = self._admission_data.exams

        doc.line(self._subheader, f"Krok {self._num_steps}")
        doc.line(self._subsubheader, "NABÍDKY")

        with doc.tag("table", klass="admission-table naive-mechanism-table"):
            with doc.tag("tr"):
                doc.line("th", "")
                for sch in schools:
                    with doc.tag("th", klass="exam-school"):
                        doc.line("i", "", klass="bi bi-house-fill")
                        doc.text(f"  {sch}")
                        doc.stag("br")
                        doc.line(
                            "small",
                            f"Míst = {self._admission_data.seats[sch]}",
                            style="font-weight: normal;",
                        )
            for i in range(max_exam_len):
                with doc.tag("tr"):
                    doc.line("th", f"{i + 1}.")
                    for sch in schools:
                        st = self._admission_data.exams[sch][i]
                        if st in self._prev_accepted[sch]:
                            extra_klass = "accepted"
                        elif st in self._prev_removed[sch]:
                            extra_klass = "not-evaluated"
                        elif st in offers and sch in offers[st]:
                            extra_klass = "offered"
                        else:
                            extra_klass = "removed"
                        # extra_klass = (
                        #     "offered"
                        #     if st in offers and sch in offers[st]
                        #     else "removed"
                        # )
                        with doc.tag("td", klass=f"exam-student {extra_klass}"):
                            doc.line("i", "", klass="bi bi-person-fill")
                            doc.text(f"  {st}")

        doc.line(self._subsubheader, "PŘIJATÉ A ODMÍTNUTÉ")

        with doc.tag("table", klass="admission-table naive-mechanism-table"):
            with doc.tag("tr"):
                doc.line("th", "")
                for sch in schools:
                    with doc.tag("th", klass="exam-school"):
                        doc.line("i", "", klass="bi bi-house-fill")
                        doc.text(f"  {sch}")
                        doc.stag("br")
                        doc.line(
                            "small",
                            f"Míst = {self._admission_data.seats[sch]}",
                            style="font-weight: normal;",
                        )
            for i in range(max_exam_len):
                with doc.tag("tr"):
                    doc.line("th", f"{i + 1}.")
                    for sch in schools:
                        st = self._admission_data.exams[sch][i]
                        if st in self._prev_accepted[sch]:
                            extra_klass = "accepted"
                        elif st in self._prev_removed[sch]:
                            extra_klass = "not-evaluated"
                        elif st in accepted[sch]:
                            extra_klass = "accepted"
                            self._prev_accepted[sch].add(st)
                        elif st in all_accepted or not remaining_seats[sch]:
                            extra_klass = "not-evaluated"
                            self._prev_removed[sch].add(st)
                        else:
                            extra_klass = ""
                        with doc.tag("td", klass=f"exam-student {extra_klass}"):
                            doc.line("i", "", klass="bi bi-person-fill")
                            doc.text(f"  {st}")

    def log_step_cermat(self, data: Mapping):
        """
        What do I want to do here?
        - probably print up the
        """
        self.doc.line("p", f"krok {self._num_steps}")
        ...
