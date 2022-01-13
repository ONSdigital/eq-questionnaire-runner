from wtforms import validators

from app.forms import error_messages
from app.forms.field_handlers.string_handler import StringHandler
from app.forms.validators import ResponseRequired


def test_get_mandatory_validator_optional(value_source_resolver, rule_evaluator):
    answer = {"mandatory": False}

    text_area_handler = StringHandler(
        answer, value_source_resolver, rule_evaluator, error_messages
    )
    validate_with = text_area_handler.get_mandatory_validator()

    assert isinstance(validate_with, validators.Optional)


def test_get_mandatory_validator_mandatory(value_source_resolver, rule_evaluator):
    answer = {"mandatory": True}

    text_area_handler = StringHandler(
        answer,
        value_source_resolver,
        rule_evaluator,
        {"MANDATORY_TEXTFIELD": "This is the default mandatory message"},
    )
    validate_with = text_area_handler.get_mandatory_validator()

    assert isinstance(validate_with, ResponseRequired)
    assert validate_with.message == "This is the default mandatory message"


def test_get_mandatory_validator_mandatory_with_error(
    value_source_resolver, rule_evaluator
):
    answer = {
        "mandatory": True,
        "validation": {
            "messages": {
                "MANDATORY_TEXTFIELD": "This is the mandatory message for an answer"
            }
        },
    }

    text_area_handler = StringHandler(
        answer, value_source_resolver, rule_evaluator, error_messages
    )
    validate_with = text_area_handler.get_mandatory_validator()

    assert isinstance(validate_with, ResponseRequired)
    assert validate_with.message == "This is the mandatory message for an answer"


def test_get_mandatory_validator_mandatory_with_question_in_error(
    value_source_resolver, rule_evaluator
):
    answer = {
        "mandatory": True,
        "validation": {
            "messages": {
                "MANDATORY_TEXTFIELD": "Select an answer to ‘%(question_title)s’"
            }
        },
    }
    text_area_handler = StringHandler(
        answer,
        value_source_resolver,
        rule_evaluator,
        {"MANDATORY_TEXTFIELD": "This is the default mandatory message"},
        question_title="To be or not to be?",
    )
    validate_with = text_area_handler.get_mandatory_validator()

    assert isinstance(validate_with, ResponseRequired)
    assert validate_with.message == "Select an answer to ‘To be or not to be?’"
