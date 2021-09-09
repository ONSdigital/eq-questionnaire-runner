from wtforms import validators

from app.data_models.answer_store import AnswerStore
from app.data_models.list_store import ListStore
from app.forms.field_handlers.string_handler import StringHandler
from app.forms.validators import ResponseRequired


def test_get_mandatory_validator_optional(mock_schema):
    answer = {"mandatory": False}

    text_area_handler = StringHandler(
        answer, mock_schema, AnswerStore(), ListStore(), {}
    )
    validate_with = text_area_handler.get_mandatory_validator()

    assert isinstance(validate_with, validators.Optional)


def test_get_mandatory_validator_mandatory(mock_schema):
    answer = {"mandatory": True}
    mock_schema.error_messages = {
        "MANDATORY_TEXTFIELD": "This is the default mandatory message"
    }
    text_area_handler = StringHandler(
        answer,
        mock_schema,
        AnswerStore(),
        ListStore(),
        {},
    )
    validate_with = text_area_handler.get_mandatory_validator()

    assert isinstance(validate_with, ResponseRequired)
    assert validate_with.message == "This is the default mandatory message"


def test_get_mandatory_validator_mandatory_with_error(mock_schema):
    answer = {
        "mandatory": True,
        "validation": {
            "messages": {
                "MANDATORY_TEXTFIELD": "This is the mandatory message for an answer"
            }
        },
    }

    mock_schema.error_messages = {
        "MANDATORY_TEXTFIELD": "This is the default mandatory message"
    }
    text_area_handler = StringHandler(
        answer,
        mock_schema,
        AnswerStore(),
        ListStore(),
        {},
    )
    validate_with = text_area_handler.get_mandatory_validator()

    assert isinstance(validate_with, ResponseRequired)
    assert validate_with.message == "This is the mandatory message for an answer"


def test_get_mandatory_validator_mandatory_with_question_in_error(mock_schema):
    answer = {
        "mandatory": True,
        "validation": {
            "messages": {
                "MANDATORY_TEXTFIELD": "Select an answer to ‘%(question_title)s’"
            }
        },
    }
    mock_schema.error_messages = {
        "MANDATORY_TEXTFIELD": "This is the default mandatory message"
    }
    text_area_handler = StringHandler(
        answer,
        mock_schema,
        AnswerStore(),
        ListStore(),
        metadata={},
        question_title="To be or not to be?",
    )
    validate_with = text_area_handler.get_mandatory_validator()

    assert isinstance(validate_with, ResponseRequired)
    assert validate_with.message == "Select an answer to ‘To be or not to be?’"
