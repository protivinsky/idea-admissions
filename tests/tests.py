import sys
sys.path.append('/home/thomas/code/idea/admissions')

from admissions.mechanism import Mechanism, DeferredAcceptance
from admissions.data import example_1, example_2, example_cermat


da1 = DeferredAcceptance(example_1)
alloc1 = da1.evaluate()

print(alloc1)

