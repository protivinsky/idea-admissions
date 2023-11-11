import sys

# figure out better way later
sys.path.append("/home/thomas/code/idea/admissions")

import textwrap
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

# all are factories
# mechanisms = [NaiveMechanism, DeferredAcceptance, CermatMechanism, SchoolOptimalSM]
mechanisms = [DeferredAcceptance, NaiveMechanism, SchoolOptimalSM]
examples = [example_1, example_2, example_3, example_4, example_cermat]
# examples = [example_1]

title = "Srovnání párovacích mechanismů pro přijímačky"
doc = rt.Doc(max_width=1200, title=title)
doc.line("h1", title)
sw = rt.Switcher()

for mechanism in mechanisms:
    for example in examples:
        logger = GraphicLogger()
        logger.doc.md(textwrap.dedent(mechanism.__doc__))
        logger.doc.md(textwrap.dedent(example.__doc__ or ""))
        mech = mechanism(example(), logger=logger)
        mech.evaluate()
        sw[mechanism.__name__][example.__name__] = logger.doc

doc.switcher(sw)
doc.save(path=".")
