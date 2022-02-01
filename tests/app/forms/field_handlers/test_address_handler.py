from werkzeug.datastructures import MultiDict
from wtforms import Form, FormField
from wtforms.validators import InputRequired

from app.forms import error_messages
from app.forms.field_handlers import AddressHandler


def get_test_form_class(
    answer_schema, value_source_resolver, rule_evaluator, messages=error_messages.copy()
):
    address_handler = AddressHandler(
        answer_schema, value_source_resolver, rule_evaluator, error_messages=messages
    )

    class TestForm(Form):
        test_field = address_handler.get_field()

    return TestForm


def test_address_fields(value_source_resolver, rule_evaluator):
    answer_json = {"id": "address", "mandatory": True, "type": "Address"}
    address_handler = AddressHandler(
        answer_json, value_source_resolver, rule_evaluator, error_messages
    )

    class TestForm(Form):
        test_field = address_handler.get_field()

    form = TestForm()

    assert isinstance(form.test_field, FormField)

    address_fields = ["line1", "line2", "town", "postcode", "uprn"]
    assert all(field in form.test_field.data for field in address_fields)


def test_address_mandatory_line1_validator(value_source_resolver, rule_evaluator):
    answer_json = {"id": "address", "mandatory": True, "type": "Address"}
    address_handler = AddressHandler(
        answer_json,
        value_source_resolver,
        rule_evaluator,
        error_messages=error_messages,
    )

    validator = address_handler.validators

    assert isinstance(validator[0], InputRequired)
    assert validator[0].message == "Enter an address"


def test_no_validation_when_address_not_mandatory(
    value_source_resolver, rule_evaluator
):
    answer_json = {"id": "address", "mandatory": False, "type": "Address"}

    test_form_class = get_test_form_class(
        answer_json, value_source_resolver, rule_evaluator
    )
    form = test_form_class(
        MultiDict({"test_field": "1"}),
        value_source_resolver,
    )
    form.validate()
    # pylint: disable=no-member
    # wtforms Form parents are not discoverable in the 2.3.3 implementation
    assert not form.errors


def test_mandatory_validation_when_address_line_1_missing(
    value_source_resolver, rule_evaluator
):
    answer_json = {"id": "address", "mandatory": True, "type": "Address"}

    test_form_class = get_test_form_class(
        answer_json, value_source_resolver, rule_evaluator
    )
    form = test_form_class(MultiDict({"test_field": "1"}), value_source_resolver)
    form.validate()
    # pylint: disable=no-member
    # wtforms Form parents are not discoverable in the 2.3.3 implementation
    assert form.errors["test_field"]["line1"][0] == "Enter an address"


def test_address_validator_with_message_override(value_source_resolver, rule_evaluator):
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
        answer_json, value_source_resolver, rule_evaluator, error_messages
    )

    validator = address_handler.validators

    assert validator[0].message == "Please enter an address line 1 to continue"
