"""Bootstrap import smoke tests."""

from fxlab import __version__
from fxlab.cli.main import build_parser


def test_package_imports() -> None:
    assert __version__ == "0.1.0"
    assert build_parser().prog
