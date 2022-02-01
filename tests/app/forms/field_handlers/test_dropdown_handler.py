import pytest
from wtforms import Form, SelectField

from app.forms import error_messages
from app.forms.field_handlers.dropdown_handler import DropdownHandler
from tests.app.forms.field_handlers.conftest import (
    dynamic_answer_options_choices,
    dynamic_answer_options_schema,
    static_and_dynamic_answer_options_choices,
    static_and_dynamic_answer_options_schema,
    static_answer_options_choices,
    static_answer_options_schema,
)


def get_dropdown_answer_schema(options):
    return {
        "type": "Dropdown",
        "id": "dropdown-with-label-answer",
        "mandatory": False,
        "label": "Please choose an option",
        "description": "This is an optional dropdown",
        **options,
    }


@pytest.mark.parametrize(
    "answer_options, choices",
    [
        (static_answer_options_schema(), static_answer_options_choices()),
        (dynamic_answer_options_schema(), dynamic_answer_options_choices()),
        (
            static_and_dynamic_answer_options_schema(),
            static_and_dynamic_answer_options_choices(),
        ),
    ],
)
def test_build_choices_without_placeholder(
    answer_options, choices, value_source_resolver, rule_evaluator
):
    dropdown_answer_schema = get_dropdown_answer_schema(answer_options)
    handler = DropdownHandler(
        dropdown_answer_schema, value_source_resolver, rule_evaluator, error_messages
    )

    expected_choices = [("", "Select an answer")] + choices

    assert handler.choices == expected_choices


@pytest.mark.parametrize(
    "answer_options, choices",
    [
        (static_answer_options_schema(), static_answer_options_choices()),
        (dynamic_answer_options_schema(), dynamic_answer_options_choices()),
        (
            static_and_dynamic_answer_options_schema(),
            static_and_dynamic_answer_options_choices(),
        ),
    ],
)
def test_build_choices_with_placeholder(
    answer_options, choices, value_source_resolver, rule_evaluator
):
    dropdown_answer_schema = get_dropdown_answer_schema(answer_options)
    dropdown_answer_schema["placeholder"] = "Select an option"
    handler = DropdownHandler(
        dropdown_answer_schema, value_source_resolver, rule_evaluator, error_messages
    )

    expected_choices = [("", "Select an option")] + choices

    assert handler.choices == expected_choices


@pytest.mark.parametrize(
    "answer_options, choices",
    [
        (static_answer_options_schema(), static_answer_options_choices()),
        (dynamic_answer_options_schema(), dynamic_answer_options_choices()),
        (
            static_and_dynamic_answer_options_schema(),
            static_and_dynamic_answer_options_choices(),
        ),
    ],
)
def test_get_field(answer_options, choices, value_source_resolver, rule_evaluator):
    dropdown_answer_schema = get_dropdown_answer_schema(answer_options)
    handler = DropdownHandler(
        dropdown_answer_schema, value_source_resolver, rule_evaluator, error_messages
    )

    expected_choices = [("", "Select an answer")] + choices

    class TestForm(Form):
        test_field = handler.get_field()

    form = TestForm()

    assert isinstance(form.test_field, SelectField)
    assert form.test_field.label.text == dropdown_answer_schema["label"]
    assert form.test_field.description == ""
    assert form.test_field.default == ""
    assert form.test_field.choices == expected_choices
