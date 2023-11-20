import os
import sys

# figure out better way later
sys.path.append("/home/thomas/code/idea/admissions")

import textwrap
import admissions
from admissions import (
    NaiveMechanism,
    DeferredAcceptance,
    CermatMechanism,
    SchoolOptimalSM,
)
from admissions.logger import GraphicLogger
from admissions.data import example_1, example_2, example_3, example_4, example_cermat
import admissions.reportree as rt

"""
Pro každý mechanismus vytiskni na obrazkovku textově jeho průběh po jednotlivých krocích.
"""

mechanisms = {
    "Mechanismus odloženého přijetí": DeferredAcceptance,
    "Mechanismus představený Cermatem": CermatMechanism,
    "Naivní mechanismus": NaiveMechanism,
    "Stabilní mechanismus optimální pro školy": SchoolOptimalSM,
}

# all are factories
# mechanisms = [NaiveMechanism, DeferredAcceptance, CermatMechanism, SchoolOptimalSM]
examples = [example_cermat, example_3, example_4, example_1]
# examples = [example_1]

title = "Studie IDEA: Přijímačky na střední školy: promyšlený mechanismus nebo velká národní loterie?"
intro_text = [
    'Tato stránka obsahuje doplňující analytický materiál autora studie <a href="https://idea.cerge-ei.cz/studies/prijimacky-na-stredni-skoly-promysleny-mechanismus-nebo-velka-narodni-loterie" target="_blank"><b>Přijímačky na střední školy: promyšlený mechanismus nebo velká národní loterie?</b></a> publikované think-tankem <a href="https://idea.cerge-ei.cz" target="_blank"><b>IDEA při CERGE-EI</b></a>. Zdrojový kód stránky s ukázkovou implementací těchto mechanismů je k dispozici na <a href="https://github.com/protivinsky/idea-admissions" target="_blank">githubu</a>. Uvítám komentáře a inspirativní nápady <a id="contact" href="">e-mailem</a>.',
    "Pro jaro 2024 je plánovaná reforma přijímacích zkoušek na střední školy, aby se zabránilo podobnému chaosu jako v roce 2023. Chystané změny jsou krok dobrým směrem, avšak stále panují nejasnosti ohledně algoritmu, který vyhodnotí data z přihlášek a výsledky zkoušek a přiřadí žáky na školy.",
    "Tento algoritmu (zvaný párovací mechanismus) není nepodstatný technický detail, ale má zásadní vliv na to, kteří žáci se na své vybrané školy dostanou a kteří nikoli.",
    "Vědci po celém světě tyto algoritmy studují již desítky let a rozlišili několik základních mechanismů. <b>Mechanismus odloženého přijetí</b> je dnes ve světě nejčastěji zaváděným systémem zkoušek a jeho kvalita je ověřena praxí i matematickými důkazy.",
    "Důrazně doporučujeme, aby MŠMT pro následující přijímací zkoušky využilo právě tento mechanismus: nepředstavuje žádnou dodatečnou zátěž a nabízí žákům jednoznačně lepší přiřazení do škol při plném respektování výsledků zkoušek.",
    'Jednotlivé podstránky ukazují průběh vybraných algoritmů na různých modelových situacích, aby ilustrovaly jejich silné a slabé stránky. První dva příklady, <i>"Zadáni dle Cermatu"</i> a <i>"Optimalita pro studenty vs. pro školy"</i> jasně ukazují, proč je mechanismus odloženého přijetí lepší než zvažovaná alternativa.',
]

doc = rt.Doc(max_width=1200, title=title)
with doc.tag("div", klass="container"):
    with doc.tag("div", klass="row"):
        with doc.tag("div", klass="col-8"):
            doc.line("h1", "Autorský analytický doplněk", klass="display-4")
            with doc.tag("h2", style="text-align: left;"):
                doc.line(
                    "a",
                    title,
                    href="https://idea.cerge-ei.cz/studies/prijimacky-na-stredni-skoly-promysleny-mechanismus-nebo-velka-narodni-loterie",
                    target="_blank",
                    style="text-decoration: none",
                )
        with doc.tag("div", klass="col-4 my-4 mr-4 d-flex justify-content-end"):
            with doc.tag("a", href="https://idea.cerge-ei.cz", target="_blank"):
                root_dir = os.path.dirname(os.path.dirname(__file__))
                image_file = os.path.join(
                    root_dir, "admissions", "reportree", "assets", "idea_logo.png"
                )
                doc.image_as_b64(image_file, width="300px")

    sw = rt.Switcher()

    doc_intro = rt.Doc()
    with doc_intro.tag("div", klass="row"):
        with doc_intro.tag("div", klass="col-12"):
            doc_intro.line("h2", "Úvod")
        with doc_intro.tag("div", klass="col-12"):
            with doc_intro.tag("ul", klass="list-unstyled"):
                for text in intro_text:
                    with doc_intro.tag("li"):
                        with doc_intro.tag("p", klass="lead"):
                            doc_intro.line("i", "", klass="bi bi-chevron-double-right")
                            doc_intro.asis(text)
        with doc_intro.tag("div", klass="col-12"):
            with doc_intro.tag("div", klass="alert alert-warning", role="alert"):
                doc_intro.text(
                    "Tento obsah je automaticky generovaný a může se v budoucnu měnit. Stránka je optimalizovaná především pro zobrazení na klasických monitorech a nemusí být plně přehledná na mobilních zařízeních."
                )

    # embed IDEA Talks YouTube video presenting the report
    with doc_intro.tag("div", klass="row mb-4"):
        with doc_intro.tag("div", klass="col-12"):
            doc_intro.line("h2", "IDEA Talks")
        with doc_intro.tag("div", klass="col-12"):
            doc_intro.line(
                "p",
                "Rozhovor s autorem studie, ve kterém popisuje některé párovací mechanismy a uvádí další návrhy pro zlepšení organizace přijímacích zkoušek na střední školy.",
                klass="lead",
            )
        doc_intro.line("div", "", klass="col-xl-2 col-lg-1")
        with doc_intro.tag("div", klass="col-xl-8 col-lg-10 col-12"):
            with doc_intro.tag("div", klass="ratio ratio-16x9"):
                doc_intro.line(
                    "iframe",
                    "",
                    src="https://www.youtube-nocookie.com/embed/ixxIDtQhV6Y",
                    title="YouTube video player",
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture",
                    allowfullscreen="allowfullscreen",
                )
        doc_intro.line("div", "", klass="col-xl-2 col-lg-1")
    doc_intro.md(textwrap.dedent(admissions.__doc__))

    sw["Úvod"] = doc_intro

    for example in examples:
        for mech_label, mechanism in mechanisms.items():
            ex_label = (
                example.__doc__.split("\n")[1] if example.__doc__ is not None else ""
            )
            logger = GraphicLogger()
            logger.doc.md(textwrap.dedent(example.__doc__ or ""))
            logger.doc.md(textwrap.dedent(mechanism.__doc__))
            mech = mechanism(example(), logger=logger)
            mech.evaluate()
            sw[ex_label][mech_label] = logger.doc

    doc.switcher(sw)

# FOOTER
with doc.tag("div", klass="container"):
    with doc.tag("div", klass="row my-8"):
        with doc.tag("div", klass="col"):
            doc.asis("&nbsp;")
with doc.tag("footer", id="footer", klass="page-footer"):
    with doc.tag("div", klass="container"):
        with doc.tag("div", klass="row d-flex align-items-center"):
            with doc.tag("div", klass="col-md-5 my-8 mr-4"):
                with doc.tag("a", href="https://idea.cerge-ei.cz", target="_blank"):
                    root_dir = os.path.dirname(os.path.dirname(__file__))
                    image_file = os.path.join(
                        root_dir, "admissions", "reportree", "assets", "idea_logo.png"
                    )
                    doc.image_as_b64(image_file, width="180px")
            with doc.tag("div", klass="col-md-6"):
                with doc.tag("b"):
                    doc.asis("&copy; 2023, Tomáš Protivínský, ")
                    doc.line("a", "", id="contact-footer", href="")
                doc.stag("br")
                doc.text(
                    "Zdrojový kód s ukázkovou implementací těchto mechanismů je k dispozici na "
                )
                doc.line(
                    "a",
                    "githubu",
                    href="https://github.com/protivinsky/idea-admissions",
                    target="_blank",
                )
                doc.text(".")
            with doc.tag(
                "div", klass="col-md-1 mr-4 d-flex justify-content-end footer-github"
            ):
                with doc.tag(
                    "a",
                    href="https://github.com/protivinsky/idea-admissions",
                    target="_blank",
                ):
                    doc.line("i", "", klass="bi bi-github")

with doc.tag("script"):
    doc.asis(
        """
// email address
var x = "dG9tYXMucHJvdGl2aW5za3lAY2VyZ2UtZWkuY3o=";
const c = document.getElementById("contact");
c.setAttribute("href", "mailto:".concat(atob(x)));
const cf = document.getElementById("contact-footer")
cf.setAttribute("href", "mailto:".concat(atob(x)));
cf.textContent = atob(x)
"""
    )

doc.save(path="output")
