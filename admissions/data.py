from .domain import AdmissionData


_RENAME = True

# names of schools and students for the simple examples
_school_names = {
    "A": "Gymnázium Nymburk",
    "B": "Lyceum Mělník",
    "C": "OA Kladno",
    "D": "SOŠ Smíchov",
}

_student_names = {
    1: "Adam",
    2: "Bára",
    3: "Cecílie",
    4: "Dan",
}


def example_1():
    """
    Příklad ze studie IDEA
    ----------------------
    Hlavní příklad ze studie, který jasně ukazuje nestabilitu (opodstatněnou závist)
    u naivního mechanismu. Stabilní mechanismy (DA, Cermat, School-optimal SM) toto zadání
    vyřeší uspokojivě.
    """
    admission_data = AdmissionData(
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
    if _RENAME:
        return admission_data.rename(
            student_names=_student_names, school_names=_school_names
        )
    else:
        return admission_data


def example_2():
    """
    Příklad 2
    ---------
    Doplňující příklad ze studie (zde není podstatný).
    """
    admission_data = AdmissionData(
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
    if _RENAME:
        return admission_data.rename(
            student_names=_student_names, school_names=_school_names
        )
    else:
        return admission_data


def example_3():
    """
    Příklad: optimalita pro studenty vs. pro školy
    ----------------------------------------------
    Příklad je záměrně navržený tak, aby zvýraznil rozdíly mezi:

    - mechanismem odloženého přijetí (**optimální pro studenty**) a
    - Cermatem navrženým mechanismem bez dodatečných optimalizací (**optimální pro školy**).

    Oba mechanismy zde vedou ke stabilnímu výsledku bez opodstatněné závisti, i tak jsou mezi
    výsledky zásadní rozdíly.
    Mechanismus odloženého přijetí přiřadí všechny žáky podle jejich první volby, zatímco mechanismus
    představený Cermatem přiřadí žáky na jejich poslední volby z přihlášek.
    """
    admission_data = AdmissionData(
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
    if _RENAME:
        return admission_data.rename(
            student_names=_student_names, school_names=_school_names
        )
    else:
        return admission_data


def example_4():
    """
    Příklad: nedosažitelnost stability a efektivity
    -----------------------------------------------
    Příklad ilustruje, že není možné zároveň dosáhnout **stability** (neexistence opodstatněné závisti)
    a **Pareto efektivity** pro studenty.

    Všechny zde uvedené mechanismy přiřadí Adama na Gymnázium Nymburk a Báru na Lyceum Mělník,
    ačkoli oba žáci by preferovali si tyto školy vzájemně vyměnit. Tím by byla zvýšena Pareto efektivita
    pro žáky (oba by si polepšili a nikdo jiný by nebyl přímo poškozený).

    Stabilní mechanismy však tuto výměnu neumožňují, neboť by vznikla opodstatněná závist (a tedy byla
    porušena stabilita): Bára nemůže být přijata na Gymnázium Nymburk, neboť Cecílie se tam také hlásila,
    byla úspěšnější v přijímací zkoušce a měla tuto školu na první pozici na přihlášce.

    **Mechanismus odloženého přijetí** je nejvíce Pareto efektivní pro studenty ze všech stabilních mechanismů
    (tzv. **optimálně stabilní**).

    Maximální efektivity pro studenty by zde dosáhl **mechanismus efektivních přesunů** (uváděný pouze
    ve studii), který však není stabilní.
    """
    admission_data = AdmissionData(
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
    if _RENAME:
        return admission_data.rename(
            student_names=_student_names, school_names=_school_names
        )
    else:
        return admission_data


def example_cermat():
    """
    Zadání dle Cermatu
    ------------------
    Tento příklad použil Cermat při vysvětlování jimi navrhnutého algoritmu.
    Jedná se o více realistický příklad, který zároveň ilustruje některé zajímavé vlastnosti.

    Mechanismus představený Cermatem, který je stabilní a optimální pro školy, zde v původní
    verzi nemůže dosáhnout tak dobrého výsledku z pohledu studentů jako mechanismus odloženého
    přijetí, který je stabilní a optimální pro studenty.

    **Mechanismus odloženého přijetí umístí 6 žáků na jejich první volbu z přihlášek a nikoho
    na poslední třetí volbu**, oproti tomu **neoptimalizovaný mechanismus dle Cermatu umístí
    pouze 4 žáky na jejich první volbu a 2 žáky na jejich poslední školy** z přihlášek. Zároveň oba
    mechanismy **plně respektují pořadí výsledků zkoušek** a nemůže se stát, že by se žák s horším výsledkem
    dostal na pozici před žáka s lepším výsledkem ze zkoušky.

    **Matematicky bylo dokázáno již v roce 1962, že mechanismus odloženého přijetí je pro žáky
    nejlepším spravedlivým mechanismem.**
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
