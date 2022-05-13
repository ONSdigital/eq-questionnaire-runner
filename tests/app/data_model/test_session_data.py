import pytest

from app.data_models import SessionData


def test_session_data_default_properties():
    try:
        session_data = SessionData(
            tx_id="123",
            schema_name="some_schema_name",
            period_str=None,
            language_code="cy",
            launch_language_code="en",
            ru_name=None,
            ru_ref=None,
            response_id="321",
            case_id="789",
        )
    except TypeError:
        return pytest.fail("An error occurred when creating session data")

    assert session_data.case_ref is None
    assert session_data.account_service_base_url is None
    assert session_data.account_service_log_out_url is None
    assert session_data.trad_as is None
    assert session_data.display_address is None
    assert session_data.confirmation_email_count == 0
    assert session_data.feedback_count == 0
    assert session_data.schema_url is None
    assert session_data.survey_url is None


def test_session_data_survey_url_always_set_to_none():
    session_data = SessionData(
        tx_id="123",
        schema_name="some_schema_name",
        period_str=None,
        language_code="cy",
        launch_language_code="en",
        ru_name=None,
        ru_ref=None,
        response_id="321",
        case_id="789",
        survey_url="some-url",
    )

    assert session_data.survey_url is None
