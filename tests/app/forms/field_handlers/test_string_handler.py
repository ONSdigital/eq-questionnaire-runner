from unittest.mock import MagicMock

from wtforms import Form, StringField, validators

from app.data_models.answer_store import AnswerStore
from app.data_models.list_store import ListStore
from app.forms.field_handlers.string_handler import StringHandler


def test_string_field(mock_schema):
    textfield_json = {
        "id": "job-title-answer",
        "label": "Job title",
        "mandatory": False,
        "guidance": "<p>Please enter your job title in the space provided.</p>",
        "type": "TextField",
    }
    string_handler = StringHandler(
        textfield_json, mock_schema, AnswerStore(), ListStore(), disable_validation=True
    )

    class TestForm(Form):
        test_field = string_handler.get_field()

    form = TestForm()

    assert isinstance(form.test_field, StringField)
    assert form.test_field.label.text == textfield_json["label"]
    assert form.test_field.description == textfield_json["guidance"]


def test_get_length_validator(mock_schema):
    string_handler = StringHandler({}, mock_schema, AnswerStore(), ListStore())

    validator = string_handler.get_length_validator

    assert isinstance(validator, validators.Length)


def test_get_length_validator_with_message_override(mock_schema):
    answer = {
        "validation": {"messages": {"MAX_LENGTH_EXCEEDED": "The message is too long!"}}
    }
    mock_schema.error_messages = {
        "MAX_LENGTH_EXCEEDED": "This is the default max length message"
    }
    string_handler = StringHandler(answer, mock_schema, AnswerStore(), ListStore())

    validator = string_handler.get_length_validator

    assert validator.message == "The message is too long!"


def test_get_length_validator_with_max_length_override(mock_schema):
    answer = {"max_length": 30}

    string_handler = StringHandler(answer, mock_schema, AnswerStore(), ListStore())
    validator = string_handler.get_length_validator

    assert validator.max == 30
