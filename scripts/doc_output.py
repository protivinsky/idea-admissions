import sys

# figure out better way later
sys.path.append("/home/thomas/code/idea/admissions")

from admissions import NaiveMechanism
from admissions.logger import DocLogger
from admissions.data import example_1, example_2, example_3, example_4, example_cermat
import admissions.reportree as rt

"""
Pro každý mechanismus vytiskni na obrazkovku textově jeho průběh po jednotlivých krocích.
"""

# all are factories
mechanisms = [NaiveMechanism]
examples = [example_1, example_2, example_3, example_4, example_cermat]

title="Admission Mechanism Comparison"
doc = rt.Doc(max_width=1200, title=title) 
doc.line("h1", title)
sw = rt.Switcher()

for mechanism in mechanisms:
    for example in examples:
        logger = DocLogger(title=f"{mechanism.__name__} [{example.__name__}]")
        logger.doc.line("h1", f"{mechanism.__name__} [{example.__name__}]")
        mech = mechanism(example(), logger=logger)
        mech.evaluate()
        sw[mechanism.__name__][example.__name__] = doc

doc.switcher(sw)
doc.save(path=".")

