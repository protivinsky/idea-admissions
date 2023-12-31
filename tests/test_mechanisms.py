# import sys
# figure out better way later
# -> ok, I just need to run it from root dir
# sys.path.append("/home/thomas/code/idea/admissions")

import pytest
from admissions import (
    DeferredAcceptance,
    CermatMechanism,
    NaiveMechanism,
    SchoolOptimalSM,
)
from admissions.data import example_1, example_2, example_cermat


da_expected = [
    (example_1(), {"A": {1}, "B": {2}, "C": {3}, "D": {4}}, set()),
    (example_2(), {"A": {1}, "B": {2}, "C": {3}}, set()),
    (
        example_cermat(),
        # accepted
        {
            "Gymnázium Nymburk": {"Bára", "Dan", "Eda", "Lenka"},
            "Lyceum Mělník": {"Adam", "Hanka", "Katka"},
            "SOŠ Smíchov": {"Cecílie", "Gustav", "Ivana", "Jana", "Marek"},
        },
        # rejected
        {"Filip"},
    ),
]

cm_expected = [
    (example_1(), {"A": {1}, "B": {2}, "C": {3}, "D": {4}}, set()),
    (example_2(), {"A": {2}, "B": {1}, "C": {3}}, set()),
    (
        example_cermat(),
        # accepted
        {
            "Gymnázium Nymburk": {"Bára", "Dan", "Eda", "Jana"},
            "Lyceum Mělník": {"Adam", "Hanka", "Lenka"},
            "SOŠ Smíchov": {"Cecílie", "Gustav", "Ivana", "Katka", "Marek"},
        },
        # rejected
        {"Filip"},
    ),
]

naive_expected = [
    (example_1(), {"A": {1}, "B": {4}, "C": {3}, "D": {2}}, set()),
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
    assert cm_result.rejected == rejected, "The rejected students differ."


@pytest.mark.parametrize("data,accepted,rejected", naive_expected)
def test_naive_allocation(data, accepted, rejected):
    naive_mechanism = NaiveMechanism(data)
    naive_result = naive_mechanism.evaluate()
    assert (
        naive_result.accepted == accepted
    ), "The allocation of accepted students differs."
    assert naive_result.rejected == rejected, "The rejected students differ."


@pytest.mark.parametrize("data,accepted,rejected", cm_expected)
def test_school_optimal_sm_allocation(data, accepted, rejected):
    # the school optimal stable mechanism is fully equivalent to cermat implementation
    school_optimal_mechanism = SchoolOptimalSM(data)
    school_optimal_result = school_optimal_mechanism.evaluate()
    assert (
        school_optimal_result.accepted == accepted
    ), "The allocation of accepted students differs."
    assert school_optimal_result.rejected == rejected, "The rejected students differ."
