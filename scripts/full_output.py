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

title = (
    "Přijímačky na střední školy: promyšlený mechanismus nebo velká národní loterie?"
)
doc = rt.Doc(max_width=1200, title=title)
with doc.tag("div", klass="container"):
    with doc.tag("div", klass="row"):
        with doc.tag("div", klass="col-7"):
            doc.line("h1", "Autorský analytický doplněk", klass="display-4")
            doc.line("h3", title)
        with doc.tag("div", klass="col-5 my-4 mr-4 d-flex justify-content-end"):
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
            with doc_intro.tag("div", klass="alert alert-warning", role="alert"):
                doc_intro.text("Tato stránka nabízí doplňující obsah ke studii ")
                doc_intro.line("a", "Přijímačky na střední školy: promyšlený mechanismus nebo velká národní loterie?", href="https://idea.cerge-ei.cz/studies/prijimacky-na-stredni-skoly-promysleny-mechanismus-nebo-velka-narodni-loterie", target="_blank")
                doc_intro.text(". Jedná se o automaticky generovanou stránku nabízející detailní vhled do průběhu jednotlivých algoritmů a zde uvedený obsah se může v budoucnu měnit. Autor případně uvítá zpětnou vazbu na ")
                doc_intro.line("a", "tomas.protivinsky@cerge-ei.cz", href="mailto:tomas.protivinsky@cerge-ei.cz")
                doc_intro.text(".")

    # embed IDEA Talks YouTube video presenting the report
    with doc_intro.tag("div", klass="row mb-4"):
        with doc_intro.tag("div", klass="col-12"):
            doc_intro.line("h2", "IDEA Talks")
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
                    doc.line(
                        "a",
                        "tomas.protivinsky@cerge-ei.cz",
                        href="mailto:tomas.protivinsky@cerge-ei.cz",
                    )
                doc.stag("br")
                doc.text(
                    "Zdrojový kód s ukázkovou implementací těchto mechanismů je k dispozici na "
                )
                doc.line(
                    "a",
                    "githubu",
                    href="https://github.com/protivinsky/idea-admissions",
                    target="_blank"
                )
                doc.text(".")
            with doc.tag("div", klass="col-md-1 mr-4 d-flex justify-content-end footer-github"):
                with doc.tag("a", href="https://github.com/protivinsky/idea-admissions", target="_blank"):
                    doc.line("i", "", klass="bi bi-github")


doc.save(path="output")
