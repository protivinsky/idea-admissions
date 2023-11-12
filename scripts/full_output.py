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

title = "Mechanismy pro přijímačky na střední školy"
doc = rt.Doc(max_width=1200, title=title)
doc.line("h1", title)

sw = rt.Switcher()
doc_intro = rt.Doc()
doc_intro.md(textwrap.dedent(admissions.__doc__))
sw["Úvod"] = doc_intro

for example in examples:
    for mech_label, mechanism in mechanisms.items():
        ex_label = example.__doc__.split("\n")[1] if example.__doc__ is not None else ""
        logger = GraphicLogger()
        logger.doc.md(textwrap.dedent(example.__doc__ or ""))
        logger.doc.md(textwrap.dedent(mechanism.__doc__))
        mech = mechanism(example(), logger=logger)
        mech.evaluate()
        sw[ex_label][mech_label] = logger.doc

doc.switcher(sw)
doc.save(path="output")
