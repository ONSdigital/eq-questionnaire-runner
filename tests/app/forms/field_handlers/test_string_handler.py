from wtforms import Form, StringField, validators

from app.forms import error_messages
from app.forms.field_handlers.string_handler import StringHandler


def test_string_field(value_source_resolver, rule_evaluator):
    textfield_json = {
        "id": "job-title-answer",
        "label": "Job title",
        "mandatory": False,
        "guidance": "<p>Please enter your job title in the space provided.</p>",
        "type": "TextField",
    }
    string_handler = StringHandler(
        textfield_json,
        value_source_resolver,
        rule_evaluator,
        error_messages,
        disable_validation=True,
    )

    class TestForm(Form):
        test_field = string_handler.get_field()

    form = TestForm()

    assert isinstance(form.test_field, StringField)
    assert form.test_field.label.text == textfield_json["label"]
    assert form.test_field.description == textfield_json["guidance"]


def test_get_length_validator(value_source_resolver, rule_evaluator):
    string_handler = StringHandler(
        {}, value_source_resolver, rule_evaluator, error_messages
    )

    validator = string_handler.get_length_validator

    assert isinstance(validator, validators.Length)


def test_get_length_validator_with_message_override(
    value_source_resolver, rule_evaluator
):
    answer = {
        "validation": {"messages": {"MAX_LENGTH_EXCEEDED": "The message is too long!"}}
    }

    string_handler = StringHandler(
        answer, value_source_resolver, rule_evaluator, error_messages
    )

    validator = string_handler.get_length_validator

    assert validator.message == "The message is too long!"


def test_get_length_validator_with_max_length_override(
    value_source_resolver, rule_evaluator
):
    answer = {"max_length": 30}

    string_handler = StringHandler(
        answer, value_source_resolver, rule_evaluator, error_messages
    )
    validator = string_handler.get_length_validator

    assert validator.max == 30
