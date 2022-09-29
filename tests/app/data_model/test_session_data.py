import pytest

from app.data_models import SessionData


def test_session_data_default_properties():
    try:
        session_data = SessionData(
            language_code="cy",
        )
    except TypeError:
        return pytest.fail("An error occurred when creating session data")

    assert session_data.confirmation_email_count == 0
    assert session_data.feedback_count == 0
