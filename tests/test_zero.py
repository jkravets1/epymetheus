import pytest
from ._utils import make_randomuniverse

from epymetheus import TradeStrategy


params_seed = [42]
params_n_bars = [10, 1000]
params_n_assets = [1, 100]


class VoidStrategy(TradeStrategy):
    """Yield no trade."""
    def logic(self, universe):
        pass


@pytest.mark.parametrize('seed', params_seed)
@pytest.mark.parametrize('n_bars', params_n_bars)
@pytest.mark.parametrize('n_assets', params_n_assets)
def test_void(seed, n_bars, n_assets):
    universe = make_randomuniverse(n_bars, n_assets)

    with pytest.raises(RuntimeError):
        strategy = VoidStrategy().run(universe)
        print(strategy)
