from unittest.mock import Mock

import pytest

from app.questionnaire import QuestionnaireSchema
from app.setup import create_app


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


def set_storage_data(storage, raw_data="{}", version=1, submitted_at=None):
    storage.get_user_data = Mock(return_value=(raw_data, version, submitted_at))
