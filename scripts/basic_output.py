import sys

# figure out better way later
sys.path.append("/home/thomas/code/idea/admissions")

from admissions import NaiveMechanism
from admissions.logger import BasicLogger
from admissions.data import example_1, example_2, example_3, example_4, example_cermat

"""
Pro každý mechanismus vytiskni na obrazkovku textově jeho průběh po jednotlivých krocích.
"""

# all are factories
mechanisms = [NaiveMechanism]
logger = BasicLogger
examples = [example_1, example_2, example_3, example_4, example_cermat]

for mechanism in mechanisms:
    for example in examples:
        mech = mechanism(example(), logger=logger())
        mech.evaluate()
