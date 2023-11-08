import sys
# figure out better way later
sys.path.append('/home/thomas/code/idea/admissions')

from admissions.mechanism import DeferredAcceptance, CermatMechanism
from admissions.data import example_1, example_2, example_3, example_4

cm_adv = CermatMechanism(example_3, verbose=True)
cm_adv_alloc = cm_adv.evaluate()

cm_4 = CermatMechanism(example_4, verbose=True)
cm_4_alloc = cm_4.evaluate()

da_adv = DeferredAcceptance(example_3, verbose=True)
da_adv_alloc = da_adv.evaluate()

da_4 = DeferredAcceptance(example_4, verbose=True)
da_4_alloc = da_4.evaluate()



