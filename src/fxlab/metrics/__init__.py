"""Performance and risk metrics."""

from fxlab.metrics.equity import drawdown_series, max_drawdown, simple_return_series
from fxlab.metrics.grouped import group_trades_by_exit_reason
from fxlab.metrics.trades import expectancy, profit_factor, win_rate

__all__ = [
    "drawdown_series",
    "expectancy",
    "group_trades_by_exit_reason",
    "max_drawdown",
    "profit_factor",
    "simple_return_series",
    "win_rate",
]
