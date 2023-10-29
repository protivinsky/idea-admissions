import sys
# figure out better way later
sys.path.append('/home/thomas/code/idea/admissions')

import pytest
from admissions.mechanism import DeferredAcceptance, CermatMechanism
from admissions.data import example_1, example_2, example_cermat


da_expected = [
    (example_1, {'A': {1}, 'B': {2}, 'C': {3}, 'D': {4}}, set()),
    (example_2, {'A': {1}, 'B': {2}, 'C': {3}}, set()),
    (
        example_cermat,
        {1: set('BDEL'), 2: set('AHK'), 3: set('CGIJM')},
        {'F'},
    ),
]

cm_expected = [
    (example_1, {'A': {1}, 'B': {2}, 'C': {3}, 'D': {4}}, set()),
    (example_2, {'A': {2}, 'B': {1}, 'C': {3}}, set()),
    (
        example_cermat,
        {1: set('BDEJ'), 2: set('AHL'), 3: set('CGIKM')},
        {'F'},
    ),
]


@pytest.mark.parametrize('data,matched,unmatched', da_expected)
def test_da_allocation(data, matched, unmatched):
    da_mechanism = DeferredAcceptance(data)
    da_result = da_mechanism.evaluate()
    assert da_result.matched == matched, 'The allocation of matched students differ.'
    assert da_result.unmatched == unmatched, 'The rejected students differ.'


@pytest.mark.parametrize('data,matched,unmatched', cm_expected)
def test_cm_allocation(data, matched, unmatched):
    cm_mechanism = CermatMechanism(data)
    cm_result = cm_mechanism.evaluate()
    assert cm_result.matched == matched, 'The allocation of matched students differ.'
    assert cm_result.unmatched == unmatched, 'The rejected students differ.'



