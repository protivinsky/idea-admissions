# import sys
# figure out better way later
# -> ok, I just need to run it from root dir
# sys.path.append("/home/thomas/code/idea/admissions")

import pytest
from admissions import DeferredAcceptance, CermatMechanism
from admissions.data import example_1, example_2, example_cermat


da_expected = [
    (example_1, {"A": {1}, "B": {2}, "C": {3}, "D": {4}}, set()),
    (example_2, {"A": {1}, "B": {2}, "C": {3}}, set()),
    (
        example_cermat,
        {1: set("BDEL"), 2: set("AHK"), 3: set("CGIJM")},
        {"F"},
    ),
]

cm_expected = [
    (example_1, {"A": {1}, "B": {2}, "C": {3}, "D": {4}}, set()),
    (example_2, {"A": {2}, "B": {1}, "C": {3}}, set()),
    (
        example_cermat,
        {1: set("BDEJ"), 2: set("AHL"), 3: set("CGIKM")},
        {"F"},
    ),
]


@pytest.mark.parametrize("data,accepted,rejected", da_expected)
def test_da_allocation(data, accepted, rejected):
    da_mechanism = DeferredAcceptance(data)
    da_result = da_mechanism.evaluate()
    assert (
        da_result.accepted == accepted
    ), "The allocation of accepted students differs."
    assert da_result.rejected == rejected, "The rejected students differ."


@pytest.mark.parametrize("data,accepted,rejected", cm_expected)
def test_cm_allocation(data, accepted, rejected):
    cm_mechanism = CermatMechanism(data)
    cm_result = cm_mechanism.evaluate()
    assert (
        cm_result.accepted == accepted
    ), "The allocation of accepted students differs."
