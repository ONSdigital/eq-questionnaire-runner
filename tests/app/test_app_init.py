from app import settings
from app.setup import get_minimized_asset


def test_get_minimized_asset_with_env():
    settings.EQ_MINIMIZE_ASSETS = True
    assert "some.min.css" == get_minimized_asset("some.css")
    assert "some.min.js" == get_minimized_asset("some.js")


def test_get_minimized_asset_without_env():
    settings.EQ_MINIMIZE_ASSETS = False

    filename = "some.css"
    assert filename == get_minimized_asset(filename)

    filename = "some.js"
    assert filename == get_minimized_asset(filename)
