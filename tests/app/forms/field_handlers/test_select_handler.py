import pytest
from mock import patch
from wtforms import Form

from app.forms import error_messages
from app.forms.field_handlers import SelectHandler
from app.forms.fields import SelectFieldWithDetailAnswer


def test_coerce_str_unless_none():
    assert SelectHandler.coerce_str_unless_none(1) == "1"
    assert SelectHandler.coerce_str_unless_none("bob") == "bob"
    assert SelectHandler.coerce_str_unless_none(12323245) == "12323245"
    assert SelectHandler.coerce_str_unless_none("9887766") == "9887766"
    assert SelectHandler.coerce_str_unless_none("None") == "None"
    assert SelectHandler.coerce_str_unless_none(None) is None


def test_get_field(value_source_resolver):
    radio_json = {
        "guidance": "",
        "id": "choose-your-side-answer",
        "label": "Choose a side",
        "mandatory": True,
        "options": [
            {
                "label": "Light Side",
                "value": "Light Side",
                "description": "The light side of the Force",
            },
            {
                "label": "Dark Side",
                "value": "Dark Side",
                "description": "The dark side of the Force",
            },
            {"label": "I prefer Star Trek", "value": "I prefer Star Trek"},
            {"label": "Other", "value": "Other"},
        ],
        "q_code": "20",
        "type": "Radio",
        "validation": {"messages": {"MANDATORY_RADIO": "This answer is required"}},
    }

    handler = SelectHandler(radio_json, value_source_resolver, error_messages)

    class TestForm(Form):
        test_field = handler.get_field()

    form = TestForm()

    expected_choices = [
        (option["label"], option["value"], None) for option in radio_json["options"]
    ]

    assert isinstance(form.test_field, SelectFieldWithDetailAnswer)
    assert form.test_field.label.text == radio_json["label"]
    assert form.test_field.description == radio_json["guidance"]
    assert form.test_field.choices == expected_choices


def test_get_field_with_bad_choices(value_source_resolver):
    radio_json = {
        "id": "choose-your-side-answer",
        "label": "Choose a side",
        "mandatory": True,
        "options": [
            {
                "label": "Light Side",
                "value": "Light Side",
            },
            {
                "label": "Dark Side",
                "value": "Dark Side",
            },
            {"label": "I prefer Star Trek", "value": "I prefer Star Trek"},
            {"label": "Other", "value": "Other"},
        ],
        "type": "Radio",
    }
    with patch.object(
        SelectHandler, "build_choices_with_detail_answer_ids", return_value=[]
    ):
        handler = SelectHandler(radio_json, value_source_resolver, error_messages)

        class TestForm(Form):
            test_field = handler.get_field()

        form = TestForm()

        form.validate()
