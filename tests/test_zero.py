import pytest

from epymetheus import TradeStrategy


params_seed = [42]
params_n_bars = [10, 1000]
params_n_assets = [1, 100]
params_verbose = [True, False]


class VoidStrategy(TradeStrategy):
    """Yield no trade."""
    def logic(self, universe):
        pass


@pytest.mark.parametrize('seed', params_seed)
@pytest.mark.parametrize('n_bars', params_n_bars)
@pytest.mark.parametrize('n_assets', params_n_assets)
@pytest.mark.parametrize('verbose', params_verbose)
def test_void(seed, n_bars, n_assets, verbose, make_randomuniverse):
    universe = make_randomuniverse(n_bars, n_assets)

    with pytest.raises(RuntimeError):
        strategy = VoidStrategy().run(universe, verbose=verbose)
        print(strategy)
