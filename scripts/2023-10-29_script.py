import sys

# figure out better way later
sys.path.append("/home/thomas/code/idea/admissions")

from admissions import DeferredAcceptance, CermatMechanism, NaiveMechanism
from admissions.data import example_1, example_2, example_cermat
from admissions.logger import BasicLogger

print()
print("===============================================")
print()

cm1 = CermatMechanism(example_1(), logger=BasicLogger())
cm1.evaluate()

print()
print("===============================================")
print()

cm2 = CermatMechanism(example_2, logger=BasicLogger())
cm2.evaluate()

print()
print("===============================================")
print()

cm3 = CermatMechanism(example_cermat, verbose=True)
cm3.evaluate()

print()
print("===============================================")
print()

da1 = DeferredAcceptance(example_1, logger=BasicLogger())
da1.seats
da1.evaluate()

print()
print("===============================================")
print()

da2 = DeferredAcceptance(example_2, logger=BasicLogger())
da2.evaluate()

print()
print("===============================================")
print()

da3 = DeferredAcceptance(example_cermat, logger=BasicLogger())
da3.seats
da3.exams
da3.applications
da3.evaluate()


print()
print("===============================================")
print()


BasicLogger.__doc__

import textwrap
import markdown

foo = textwrap.dedent(NaiveMechanism.__doc__)
markdown.markdown(foo)

markdown.markdown("1. ahoj\n2. here")
