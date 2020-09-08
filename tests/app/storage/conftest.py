from datetime import datetime, timedelta

from dateutil.tz import tzutc
from pytest import fixture

from app.data_models.app_models import EQSession
from app.setup import create_app

NOW = datetime.now(tz=tzutc()).replace(microsecond=0)


@fixture
def app():
    setting_overrides = {"LOGIN_DISABLED": True}
    the_app = create_app(setting_overrides=setting_overrides)

    return the_app


@fixture
def fake_eq_session():
    eq_session = EQSession(
        eq_session_id="sessionid",
        user_id="someuser",
        session_data="somedata",
        expires_at=NOW + timedelta(minutes=1),
    )

    return eq_session
