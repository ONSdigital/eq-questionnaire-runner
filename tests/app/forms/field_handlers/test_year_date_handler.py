from wtforms import Form

from app.forms import error_messages
from app.forms.field_handlers import YearDateHandler
from app.forms.fields import YearDateField


def test_get_field(value_source_resolver, rule_evaluator):
    date_json = {
        "guidance": "",
        "id": "month-year-answer",
        "label": "Date",
        "mandatory": True,
        "type": "MonthYearDate",
        "validation": {
            "messages": {
                "INVALID_DATE": "The date entered is not valid.  Please correct your answer.",
                "MANDATORY_DATE": "Please provide an answer to continue.",
            }
        },
    }

    handler = YearDateHandler(
        date_json, value_source_resolver, rule_evaluator, error_messages
    )

    class TestForm(Form):
        test_field = handler.get_field()

    form = TestForm()

    assert isinstance(form.test_field, YearDateField)
    assert form.test_field.label.text == date_json["label"]
    assert form.test_field.description == date_json["guidance"]
