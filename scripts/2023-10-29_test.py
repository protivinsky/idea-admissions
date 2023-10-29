import sys
# figure out better way later
sys.path.append('/home/thomas/code/idea/admissions')

from admissions.mechanism import DeferredAcceptance, CermatMechanism
from admissions.data import example_1, example_2, example_cermat

print()
print('===============================================')
print()

cm1 = CermatMechanism(example_1, verbose=True)
cm1.evaluate()

print()
print('===============================================')
print()

cm2 = CermatMechanism(example_2, verbose=True)
cm2.evaluate()

print()
print('===============================================')
print()

cm3 = CermatMechanism(example_cermat, verbose=True)
cm3.evaluate()

print()
print('===============================================')
print()

da1 = DeferredAcceptance(example_1, verbose=True)
da1.evaluate()

print()
print('===============================================')
print()

da2 = DeferredAcceptance(example_2, verbose=True)
da2.evaluate()

print()
print('===============================================')
print()

da3 = DeferredAcceptance(example_cermat, verbose=True)
da3.evaluate()

print()
print('===============================================')
print()


