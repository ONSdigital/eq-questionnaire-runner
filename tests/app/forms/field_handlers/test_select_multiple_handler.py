from wtforms import Form

from app.forms.field_handlers import SelectMultipleHandler
from app.forms.fields import MultipleSelectFieldWithDetailAnswer


def test_get_field():
    checkbox_json = {
        "guidance": "",
        "id": "opening-crawler-answer",
        "label": "",
        "mandatory": False,
        "options": [
            {"label": "Luke Skywalker", "value": "Luke Skywalker"},
            {"label": "Han Solo", "value": "Han Solo"},
            {"label": "The Emperor", "value": "The Emperor"},
            {"label": "R2D2", "value": "R2D2"},
            {"label": "Senator Amidala", "value": "Senator Amidala"},
            {"label": "Yoda", "value": "Yoda"},
        ],
        "q_code": "7",
        "type": "Checkbox",
    }

    handler = SelectMultipleHandler(checkbox_json)

    class TestForm(Form):
        test_field = handler.get_field()

    form = TestForm()

    expected_choices = [
        (option["value"], option["label"], None) for option in checkbox_json["options"]
    ]

    assert isinstance(form.test_field, MultipleSelectFieldWithDetailAnswer)
    assert form.test_field.label.text == checkbox_json["label"]
    assert form.test_field.description == checkbox_json["guidance"]
    assert form.test_field.choices == expected_choices
    assert len(form.test_field.validators) == 1
