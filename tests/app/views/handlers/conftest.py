from datetime import datetime, timezone
from unittest.mock import Mock

import pytest
from freezegun import freeze_time

from app.data_models.session_data import SessionData
from app.questionnaire import QuestionnaireSchema
from app.setup import create_app

time_to_freeze = datetime.now(timezone.utc).replace(second=0, microsecond=0)


@pytest.fixture()
@freeze_time(time_to_freeze)
def session_data():
    return SessionData(
        tx_id="123",
        schema_name="some_schema_name",
        display_address="68 Abingdon Road, Goathill",
        period_str=None,
        language_code="cy",
        launch_language_code="en",
        survey_url=None,
        ru_name=None,
        ru_ref=None,
        submitted_at=datetime.now(timezone.utc).isoformat(),
        response_id="321",
        case_id="789",
    )


@pytest.fixture()
def confirmation_email_fulfilment_schema():
    return QuestionnaireSchema(
        {
            "form_type": "H",
            "region_code": "GB-WLS",
            "submission": {"confirmation_email": True},
        }
    )


@pytest.fixture
def app():
    setting_overrides = {"LOGIN_DISABLED": True}
    the_app = create_app(setting_overrides=setting_overrides)

    return the_app


@pytest.fixture
def language():
    return "en"


@pytest.fixture
def schema():
    return QuestionnaireSchema({"post_submission": {"view_response": True}})


@pytest.fixture
def storage():
    return Mock()


def set_storage_data(storage_, raw_data="{}", version=1, submitted_at=None):
    storage_.get_user_data = Mock(return_value=(raw_data, version, submitted_at))
