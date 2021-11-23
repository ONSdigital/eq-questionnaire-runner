from datetime import datetime, timezone

import pytest

from app.setup import create_app

RESPONSE_EXPIRY = datetime(2021, 11, 10, 8, 54, 22, tzinfo=timezone.utc)


@pytest.fixture
def app():
    setting_overrides = {"LOGIN_DISABLED": True}
    the_app = create_app(setting_overrides=setting_overrides)

    return the_app


@pytest.fixture
def answer_schema_dropdown():
    return {
        "type": "Dropdown",
        "id": "mandatory-checkbox-with-mandatory-dropdown-detail-answer",
        "mandatory": True,
        "label": "Please specify heat level",
        "placeholder": "Select heat level",
        "options": [
            {"label": "Mild", "value": "Mild"},
            {"label": "Medium", "value": "Medium"},
            {"label": "Hot", "value": "Hot"},
        ],
    }


@pytest.fixture
def answer_schema_number():
    return {
        "mandatory": False,
        "id": "other-answer",
        "label": "Please enter a number of items",
        "type": "Number",
        "parent_id": "checkbox-question-numeric-detail",
    }


@pytest.fixture
def answer_schema_textfield():
    return {
        "mandatory": False,
        "id": "other-answer",
        "label": "Please specify",
        "type": "TextField",
        "parent_id": "checkbox-question-textfield-detail",
    }
