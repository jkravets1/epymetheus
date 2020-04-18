import pytest  # noqa: F401

from numpy import array_equal

from epymetheus import Wealth
from epymetheus.datasets import make_randomwalk
from epymetheus.benchmarks import RandomTrader


def assert_result_equal(result0, result1):
    for (k0, v0), (k1, v1) in zip(result0.items(), result1.items()):
        assert k0 == k1
        assert array_equal(v0, v1)


# --------------------------------------------------------------------------------


def test_init():
    """
    Test if `Wealth(strategy) == strategy.wealth`.
    """
    universe = make_randomwalk()
    strategy = RandomTrader().run(universe)

    assert_result_equal(Wealth(strategy), strategy.wealth)
