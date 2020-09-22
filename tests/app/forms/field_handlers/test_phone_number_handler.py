from wtforms import Form, StringField

from app.forms.field_handlers.mobile_number_handler import MobileNumberHandler


def test_phone_number_handler():
    string_field_definition = {
        "id": "phone-number-answer",
        "label": "Phone Number",
        "guidance": "Please enter your phone number.",
        "mandatory": False,
        "type": "PhoneNumber",
    }
    phone_number_handler = MobileNumberHandler(
        string_field_definition, disable_validation=False
    )

    class TestForm(Form):
        test_field = phone_number_handler.get_field()

    form = TestForm()

    assert isinstance(form.test_field, StringField)
    assert form.test_field.label.text == string_field_definition["label"]
    assert form.test_field.description == string_field_definition["guidance"]
