import pytest
from wtforms import Form

from app.forms import error_messages
from app.forms.field_handlers import SelectMultipleHandler
from app.forms.fields import MultipleSelectFieldWithDetailAnswer
from tests.app.forms.field_handlers.conftest import (
    dynamic_answer_options_choices,
    dynamic_answer_options_schema,
    static_and_dynamic_answer_options_choices,
    static_and_dynamic_answer_options_schema,
    static_answer_options_choices,
    static_answer_options_schema,
    to_choices_with_detail_answer_id,
)


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
    checkbox_json = {
        "guidance": "",
        "id": "opening-crawler-answer",
        "label": "",
        "mandatory": False,
        "q_code": "7",
        "type": "Checkbox",
        **answer_options,
    }

    handler = SelectMultipleHandler(
        checkbox_json, value_source_resolver, rule_evaluator, error_messages
    )

    class TestForm(Form):
        test_field = handler.get_field()

    form = TestForm()

    assert isinstance(form.test_field, MultipleSelectFieldWithDetailAnswer)
    assert form.test_field.label.text == checkbox_json["label"]
    assert form.test_field.description == checkbox_json["guidance"]
    assert form.test_field.choices == to_choices_with_detail_answer_id(expected_choices)
    assert len(form.test_field.validators) == 1
