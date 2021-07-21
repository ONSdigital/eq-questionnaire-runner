from flask.app import Flask
from pytest import fixture

from app.setup import create_app


@fixture
def app() -> Flask:
    setting_overrides = {"LOGIN_DISABLED": True}
    _app = create_app(setting_overrides=setting_overrides)

    return _app
