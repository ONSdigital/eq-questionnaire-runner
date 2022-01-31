from wtforms import Form, FormField

from app.forms import error_messages
from app.forms.field_handlers.duration_handler import DurationHandler


def test_get_field(value_source_resolver, rule_evaluator):
    date_json = {
        "guidance": "",
        "id": "year-month-answer",
        "label": "Duration",
        "mandatory": True,
        "type": "Duration",
        "units": ["years", "months"],
    }
    handler = DurationHandler(
        date_json, value_source_resolver, rule_evaluator, error_messages
    )

    class TestForm(Form):
        test_field = handler.get_field()

    form = TestForm()

    assert isinstance(form.test_field, FormField)
    assert form.test_field.label.text == date_json["label"]
    assert form.test_field.description == date_json["guidance"]
