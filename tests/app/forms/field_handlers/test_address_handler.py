from werkzeug.datastructures import MultiDict
from wtforms import Form, FormField
from wtforms.validators import InputRequired

from app.data_models.answer_store import AnswerStore
from app.data_models.list_store import ListStore
from app.forms import error_messages
from app.forms.field_handlers import AddressHandler


def get_test_form_class(answer_schema, mock_schema):
    mock_schema.error_messages = error_messages
    address_handler = AddressHandler(
        answer_schema, mock_schema, AnswerStore(), ListStore()
    )

    class TestForm(Form):
        test_field = address_handler.get_field()

    return TestForm


def test_address_fields(mock_schema):
    answer_json = {"id": "address", "mandatory": True, "type": "Address"}
    address_handler = AddressHandler(
        answer_json, mock_schema, AnswerStore(), ListStore()
    )

    class TestForm(Form):
        test_field = address_handler.get_field()

    form = TestForm()

    assert isinstance(form.test_field, FormField)

    address_fields = ["line1", "line2", "town", "postcode", "uprn"]
    assert all(field in form.test_field.data for field in address_fields)


def test_address_mandatory_line1_validator(mock_schema):
    answer_json = {"id": "address", "mandatory": True, "type": "Address"}
    mock_schema.error_messages = error_messages
    address_handler = AddressHandler(
        answer_json, mock_schema, AnswerStore(), ListStore()
    )

    validator = address_handler.validators

    assert isinstance(validator[0], InputRequired)
    assert validator[0].message == "Enter an address"


def test_no_validation_when_address_not_mandatory(mock_schema):
    answer_json = {"id": "address", "mandatory": False, "type": "Address"}

    test_form_class = get_test_form_class(answer_json, mock_schema)
    form = test_form_class(MultiDict({"test_field": "1"}), mock_schema)
    form.validate()

    assert not form.errors


def test_mandatory_validation_when_address_line_1_missing(mock_schema):
    answer_json = {"id": "address", "mandatory": True, "type": "Address"}

    test_form_class = get_test_form_class(answer_json, mock_schema)
    form = test_form_class(MultiDict({"test_field": "1"}), mock_schema)
    form.validate()

    assert form.errors["test_field"]["line1"][0] == "Enter an address"


def test_address_validator_with_message_override(mock_schema):
    answer_json = {
        "id": "address",
        "mandatory": True,
        "type": "Address",
        "validation": {
            "messages": {
                "MANDATORY_ADDRESS": "Please enter an address line 1 to continue"
            }
        },
    }
    address_handler = AddressHandler(
        answer_json, mock_schema, AnswerStore(), ListStore()
    )

    validator = address_handler.validators

    assert validator[0].message == "Please enter an address line 1 to continue"
