from wtforms import Form

from app.data_models.answer_store import AnswerStore
from app.data_models.list_store import ListStore
from app.forms.field_handlers import TextAreaHandler
from app.forms.fields import MaxTextAreaField


def test_get_field(mock_schema):
    textarea_json = {
        "guidance": "",
        "id": "answer",
        "label": "Enter your comments",
        "mandatory": False,
        "q_code": "0",
        "type": "TextArea",
        "validation": {
            "messages": {
                "MAX_LENGTH_EXCEEDED": "A message with characters %(max)d placeholder"
            }
        },
    }

    text_area_handler = TextAreaHandler(
        textarea_json, mock_schema, AnswerStore(), ListStore()
    )

    class TestForm(Form):
        test_field = text_area_handler.get_field()

    form = TestForm()

    assert isinstance(form.test_field, MaxTextAreaField)
    assert form.test_field.label.text == textarea_json["label"]
    assert form.test_field.description == textarea_json["guidance"]


def test_get_length_validator(mock_schema):
    mock_schema.error_messages = {
        "MAX_LENGTH_EXCEEDED": "This is the default max length of %(max)d message"
    }
    text_area_handler = TextAreaHandler(
        {},
        mock_schema,
        ListStore(),
        AnswerStore(),
        {},
    )
    validator = text_area_handler.get_length_validator()

    assert validator.message == "This is the default max length of %(max)d message"


def test_get_length_validator_with_message_override(mock_schema):
    answer = {
        "validation": {
            "messages": {
                "MAX_LENGTH_EXCEEDED": "A message with characters %(max)d placeholder"
            }
        }
    }
    mock_schema.error_messages = {
        "MAX_LENGTH_EXCEEDED": "This is the default max length message"
    }
    text_area_handler = TextAreaHandler(
        answer,
        mock_schema,
        AnswerStore(),
        ListStore(),
        {},
    )

    validator = text_area_handler.get_length_validator()

    assert validator.message == "A message with characters %(max)d placeholder"


def test_get_length_validator_with_max_length_override(mock_schema):
    answer = {"max_length": 30}
    mock_schema.error_messages = {"MAX_LENGTH_EXCEEDED": "%(max)d characters"}
    text_area_handler = TextAreaHandler(
        answer, mock_schema, AnswerStore(), ListStore(), {}
    )
    validator = text_area_handler.get_length_validator()

    assert validator.max == 30


def test_get_text_area_rows_with_default(mock_schema):
    answer = {
        "id": "answer",
        "label": "Enter your comments",
        "mandatory": False,
        "type": "TextArea",
    }

    text_area_handler = TextAreaHandler(
        answer, mock_schema, AnswerStore(), ListStore(), disable_validation=True
    )

    class TestForm(Form):
        test_field = text_area_handler.get_field()

    form = TestForm()

    assert form.test_field.rows == 8


def test_get_text_area_rows(mock_schema):
    answer = {
        "id": "answer",
        "rows": 3,
        "label": "Enter your comments",
        "mandatory": False,
        "type": "TextArea",
    }

    text_area_handler = TextAreaHandler(
        answer, mock_schema, AnswerStore(), ListStore(), disable_validation=True
    )

    class TestForm(Form):
        test_field = text_area_handler.get_field()

    form = TestForm()

    assert form.test_field.rows == 3
