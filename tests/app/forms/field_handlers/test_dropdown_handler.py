from pytest import fixture
from wtforms import Form, SelectField

from app.forms.field_handlers.dropdown_handler import DropdownHandler


@fixture
def dropdown_answer_schema():
    return {
        "type": "Dropdown",
        "id": "dropdown-with-label-answer",
        "mandatory": False,
        "label": "Please choose an option",
        "description": "This is an optional dropdown",
        "options": [
            {"label": "Liverpool", "value": "Liverpool"},
            {"label": "Chelsea", "value": "Chelsea"},
            {"label": "Rugby is better!", "value": "Rugby is better!"},
        ],
    }


def test_build_choices_without_placeholder(dropdown_answer_schema):
    handler = DropdownHandler(dropdown_answer_schema)

    expected_choices = [("", "Select an answer")] + [
        (option["label"], option["value"])
        for option in dropdown_answer_schema["options"]
    ]

    assert handler.build_choices(dropdown_answer_schema["options"]) == expected_choices


def test_build_choices_with_placeholder(dropdown_answer_schema):
    dropdown_answer_schema["placeholder"] = "Select an option"
    handler = DropdownHandler(dropdown_answer_schema)

    expected_choices = [("", "Select an option")] + [
        (option["label"], option["value"])
        for option in dropdown_answer_schema["options"]
    ]

    assert handler.build_choices(dropdown_answer_schema["options"]) == expected_choices


def test_get_field(dropdown_answer_schema):
    handler = DropdownHandler(dropdown_answer_schema)

    expected_choices = [("", "Select an answer")] + [
        (option["label"], option["value"])
        for option in dropdown_answer_schema["options"]
    ]

    class TestForm(Form):
        test_field = handler.get_field()

    form = TestForm()

    assert isinstance(form.test_field, SelectField)
    assert form.test_field.label.text == dropdown_answer_schema["label"]
    assert form.test_field.description == ""
    assert form.test_field.default == ""
    assert form.test_field.choices == expected_choices
