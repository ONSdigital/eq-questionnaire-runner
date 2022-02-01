from wtforms import Form, StringField

from app.forms import error_messages
from app.forms.field_handlers.mobile_number_handler import MobileNumberHandler


def test_phone_number_handler(value_source_resolver, rule_evaluator):
    answer_schema = {
        "id": "phone-number-answer",
        "label": "Phone Number",
        "guidance": "Please enter your phone number.",
        "mandatory": False,
        "type": "PhoneNumber",
    }
    mobile_number_handler = MobileNumberHandler(
        answer_schema,
        value_source_resolver,
        rule_evaluator,
        error_messages,
        disable_validation=False,
    )

    class TestForm(Form):
        test_field = mobile_number_handler.get_field()

    form = TestForm()

    assert isinstance(form.test_field, StringField)
    assert form.test_field.label.text == answer_schema["label"]
    assert form.test_field.description == answer_schema["guidance"]
