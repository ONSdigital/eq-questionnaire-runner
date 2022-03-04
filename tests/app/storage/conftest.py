from datetime import datetime, timedelta, timezone

from pytest import fixture

from app.data_models.app_models import EQSession

NOW = datetime.now(tz=timezone.utc).replace(microsecond=0)


@fixture
def fake_eq_session():
    eq_session = EQSession(
        eq_session_id="sessionid",
        user_id="someuser",
        session_data="somedata",
        expires_at=NOW + timedelta(minutes=1),
    )

    return eq_session
