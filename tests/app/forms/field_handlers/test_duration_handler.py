from wtforms import Form, FormField

from app.data_models.answer_store import AnswerStore
from app.data_models.list_store import ListStore
from app.forms import error_messages
from app.forms.field_handlers.duration_handler import DurationHandler


def test_get_field(mock_schema):
    date_json = {
        "guidance": "",
        "id": "year-month-answer",
        "label": "Duration",
        "mandatory": True,
        "type": "Duration",
        "units": ["years", "months"],
    }
    mock_schema.error_messages = error_messages
    handler = DurationHandler(date_json, mock_schema, AnswerStore(), ListStore())

    class TestForm(Form):
        test_field = handler.get_field()

    form = TestForm()

    assert isinstance(form.test_field, FormField)
    assert form.test_field.label.text == date_json["label"]
    assert form.test_field.description == date_json["guidance"]
