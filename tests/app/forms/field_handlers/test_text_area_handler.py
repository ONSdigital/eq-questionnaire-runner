from wtforms import Form

from app.forms import error_messages
from app.forms.field_handlers import TextAreaHandler
from app.forms.fields import MaxTextAreaField


def test_get_field(value_source_resolver, rule_evaluator):
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
        textarea_json, value_source_resolver, rule_evaluator, error_messages
    )

    class TestForm(Form):
        test_field = text_area_handler.get_field()

    form = TestForm()

    assert isinstance(form.test_field, MaxTextAreaField)
    assert form.test_field.label.text == textarea_json["label"]
    assert form.test_field.description == textarea_json["guidance"]


def test_get_length_validator(value_source_resolver, rule_evaluator):
    test_error_messages = {
        "MAX_LENGTH_EXCEEDED": "This is the default max length of %(max)d message"
    }
    text_area_handler = TextAreaHandler(
        {}, value_source_resolver, rule_evaluator, test_error_messages
    )
    validator = text_area_handler.get_length_validator()

    assert validator.message == "This is the default max length of %(max)d message"


def test_get_length_validator_with_message_override(
    value_source_resolver, rule_evaluator
):
    answer = {
        "validation": {
            "messages": {
                "MAX_LENGTH_EXCEEDED": "A message with characters %(max)d placeholder"
            }
        }
    }
    test_error_messages = {
        "MAX_LENGTH_EXCEEDED": "This is the default max length message"
    }
    text_area_handler = TextAreaHandler(
        answer, value_source_resolver, rule_evaluator, test_error_messages
    )

    validator = text_area_handler.get_length_validator()

    assert validator.message == "A message with characters %(max)d placeholder"


def test_get_length_validator_with_max_length_override(
    value_source_resolver, rule_evaluator
):
    answer = {"max_length": 30}
    test_error_messages = {"MAX_LENGTH_EXCEEDED": "%(max)d characters"}
    text_area_handler = TextAreaHandler(
        answer, value_source_resolver, rule_evaluator, test_error_messages
    )
    validator = text_area_handler.get_length_validator()

    assert validator.max == 30


def test_get_text_area_rows_with_default(value_source_resolver, rule_evaluator):
    answer = {
        "id": "answer",
        "label": "Enter your comments",
        "mandatory": False,
        "type": "TextArea",
    }

    text_area_handler = TextAreaHandler(
        answer,
        value_source_resolver,
        rule_evaluator,
        error_messages,
        disable_validation=True,
    )

    class TestForm(Form):
        test_field = text_area_handler.get_field()

    form = TestForm()

    assert form.test_field.rows == 8


def test_get_text_area_rows(value_source_resolver, rule_evaluator):
    answer = {
        "id": "answer",
        "rows": 3,
        "label": "Enter your comments",
        "mandatory": False,
        "type": "TextArea",
    }

    text_area_handler = TextAreaHandler(
        answer,
        value_source_resolver,
        rule_evaluator,
        error_messages,
        disable_validation=True,
    )

    class TestForm(Form):
        test_field = text_area_handler.get_field()

    form = TestForm()

    assert form.test_field.rows == 3
