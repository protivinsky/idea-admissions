from .domain import Admission


example_1 = Admission(
    applications={
        1: ("A", "B", "C"),
        2: ("A", "B", "D"),
        3: ("A", "C", "D"),
        4: ("B", "C", "D"),
    },
    exams={
        "A": (1, 2, 3),
        "B": (1, 2, 4),
        "C": (1, 3, 4),
        "D": (2, 3, 4),
    },
    seats={k: 1 for k in "ABCD"},
)

example_2 = Admission(
    applications={
        1: ("A", "B", "C"),
        2: ("B", "A", "C"),
        3: ("A", "B", "C"),
    },
    exams={
        "A": (2, 1, 3),
        "B": (1, 2, 3),
        "C": (1, 2, 3),
    },
    seats={k: 1 for k in "ABC"},
)

# ex 3 - highlights the distinctions b/w DA and CM
# DA is SOSM = student-optimal stable mechanism
# CM is essentially school-optimal stable mechanism
example_3 = Admission(
    applications={
        1: ("A", "B", "C"),
        2: ("B", "C", "A"),
        3: ("C", "A", "B"),
    },
    exams={
        "A": (2, 3, 1),
        "B": (3, 1, 2),
        "C": (1, 2, 3),
    },
    seats={k: 1 for k in "ABC"},
)

# ex 4 - ETM pareto dominates DA here
example_4 = Admission(
    applications={
        1: ("B", "A", "C"),
        2: ("A", "B", "C"),
        3: ("A", "B", "C"),
    },
    exams={
        "A": (1, 3, 2),
        "B": (2, 1, 3),
        "C": (2, 1, 3),
    },
    seats={k: 1 for k in "ABC"},
)


example_cermat_school_names = {
    1: "Gymnázium Nymburk",
    2: "Lyceum Mělník",
    3: "SOŠ Smíchov",
}

example_cermat_student_list = [
    "Adam",
    "Bára",
    "Cecílie",
    "Dan",
    "Eda",
    "Filip",
    "Gustav",
    "Hanka",
    "Ivana",
    "Jana",
    "Katka",
    "Lenka",
    "Marek",
]
example_cermat_student_names = {s: s[0] for s in example_cermat_student_list}
example_cermat_exams = {
    1: tuple([s for s in "AIDMECJBLFHKG"]),
    2: tuple([s for s in "CGIAHMLKJEFDB"]),
    3: tuple([s for s in "IGBKCADMEHLJF"]),
}
example_cermat_applications = {
    "A": (2, 3, 1),
    "B": (2, 1, 3),
    "C": (3, 2, 1),
    "D": (2, 1, 3),
    "E": (2, 1, 3),
    "F": (1, 3, 2),
    "G": (1, 3, 2),
    "H": (1, 2, 3),
    "I": (3, 2, 1),
    "J": (2, 3, 1),
    "K": (2, 3, 1),
    "L": (1, 3, 2),
    "M": (3, 2, 1),
}


example_cermat = Admission(
    applications=example_cermat_applications,
    exams=example_cermat_exams,
    seats={1: 4, 2: 3, 3: 5},
    school_names=example_cermat_school_names,
    student_names=example_cermat_student_names,
)
