import pytest
from wtforms import Form

from app.forms import error_messages
from app.forms.field_handlers import SelectHandler
from app.forms.fields import SelectFieldWithDetailAnswer
from tests.app.forms.field_handlers.conftest import (
    dynamic_answer_options_choices,
    dynamic_answer_options_schema,
    static_and_dynamic_answer_options_choices,
    static_and_dynamic_answer_options_schema,
    static_answer_options_choices,
    static_answer_options_schema,
    to_choices_with_detail_answer_id,
)


def test_coerce_str_unless_none():
    assert SelectHandler.coerce_str_unless_none(1) == "1"
    assert SelectHandler.coerce_str_unless_none("bob") == "bob"
    assert SelectHandler.coerce_str_unless_none(12323245) == "12323245"
    assert SelectHandler.coerce_str_unless_none("9887766") == "9887766"
    assert SelectHandler.coerce_str_unless_none("None") == "None"
    assert SelectHandler.coerce_str_unless_none(None) is None


@pytest.mark.parametrize(
    "answer_options, expected_choices",
    [
        (static_answer_options_schema(), static_answer_options_choices()),
        (dynamic_answer_options_schema(), dynamic_answer_options_choices()),
        (
            static_and_dynamic_answer_options_schema(),
            static_and_dynamic_answer_options_choices(),
        ),
    ],
)
def test_get_field(
    answer_options, expected_choices, value_source_resolver, rule_evaluator
):
    radio_json = {
        "guidance": "",
        "id": "choose-your-side-answer",
        "label": "Choose a side",
        "mandatory": True,
        "q_code": "20",
        "type": "Radio",
        "validation": {"messages": {"MANDATORY_RADIO": "This answer is required"}},
        **answer_options,
    }

    handler = SelectHandler(
        radio_json, value_source_resolver, rule_evaluator, error_messages
    )

    class TestForm(Form):
        test_field = handler.get_field()

    form = TestForm()

    assert isinstance(form.test_field, SelectFieldWithDetailAnswer)
    assert form.test_field.label.text == radio_json["label"]
    assert form.test_field.description == radio_json["guidance"]
    assert form.test_field.choices == to_choices_with_detail_answer_id(expected_choices)
