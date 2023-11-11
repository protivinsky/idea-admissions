from .domain import AdmissionData


def example_1():
    """
    Example 1
    ---------
    Hlavní příklad ze studie, který jasně ukazuje nestabilitu (opodstatněnou závist)
    u naivního mechanismu. Stabilní mechanismy (DA, Cermat, School-optimal SM) tento
    příklad zvládnou.
    """
    return AdmissionData(
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


def example_2():
    """
    Example 2
    ---------
    Doplňující příklad ze studie (zde není podstatný).
    """
    return AdmissionData(
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


def example_3():
    """
    Example 3
    ---------
    Highlights the distinctions b/w DA and CM
    - DA is SOSM = student-optimal stable mechanism
    - CM is essentially school-optimal stable mechanism
    """
    return AdmissionData(
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


def example_4():
    """
    Example 4
    ---------
    Ilustruje situaci, kde DA nedosáhne zcela efektivního výsledku (tzn. optimálního pro studenty).
    Mechanismus efektivních transferů (zde neimplementovaný) by Pareto efektivity pro studenty dosáhl,
    avšak vyskytla by se v něm opodstatněná závist (tedy by nebyl stabilní). Tento příklad zároveň
    ilustruje, že stabilitu a maximální efektivitu pro studenty není možné naplnit zároveň.

    DA je nejvíce Pareto efektivní pro studenty mezi stabilními mechanismy (tzv. optimálně stabilní).
    """
    return AdmissionData(
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


def example_cermat():
    """
    Example Cermat
    --------------
    Tento příklad používá Cermat ve svém videu vysvětlujícím průběh přijímacích zkoušek.
    Jedná se o více realistický příklad, který zároveň ilustruje některé zajímavé vlastnosti.

    Cermat mechanism (který je school-optimal stable mechanism) zde nemůže dosáhnout efektivního
    výsledku, neboť školy preferují jiné stabilní rozřazení než žáci. Oproti tomu DA dosáhne
    stabilního výsledku, který je efektivnější z pohledu studentů.
    """
    school_names = {
        1: "Gymnázium Nymburk",
        2: "Lyceum Mělník",
        3: "SOŠ Smíchov",
    }

    student_list = [
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
    student_names = {s[0]: s for s in student_list}

    exams = {
        1: tuple([s for s in "AIDMECJBLFHKG"]),
        2: tuple([s for s in "CGIAHMLKJEFDB"]),
        3: tuple([s for s in "IGBKCADMEHLJF"]),
    }
    applications = {
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
    example_with_ids = AdmissionData(
        applications=applications,
        exams=exams,
        seats={1: 4, 2: 3, 3: 5},
    )

    example = example_with_ids.rename(
        student_names=student_names, school_names=school_names
    )
    return example
