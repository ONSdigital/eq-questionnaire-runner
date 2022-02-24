# pylint: disable=unused-argument
from werkzeug.datastructures import MultiDict
from wtforms import Form

from app.data_models.answer import Answer
from app.data_models.answer_store import AnswerStore
from app.forms import error_messages
from app.forms.field_handlers.number_handler import NumberHandler
from app.forms.fields import DecimalFieldWithSeparator, IntegerFieldWithSeparator
from app.settings import MAX_NUMBER

# pylint: disable=no-member
# wtforms Form parents are not discoverable in the 2.3.3 implementation


def get_test_form_class(
    answer_schema, value_source_resolver, rule_evaluator, messages=error_messages.copy()
):
    handler = NumberHandler(
        answer_schema, value_source_resolver, rule_evaluator, error_messages=messages
    )

    class TestForm(Form):
        test_field = handler.get_field()

    return TestForm


def test_integer_field(value_source_resolver, rule_evaluator):
    answer_schema = {
        "alias": "chewies_age",
        "guidance": "",
        "id": "chewies-age-answer",
        "mandatory": False,
        "label": "How old is Chewy?",
        "type": "Number",
        "validation": {"messages": {"INVALID_NUMBER": "Please enter your age."}},
    }

    form_class = get_test_form_class(
        answer_schema, value_source_resolver, rule_evaluator, error_messages
    )
    form = form_class()

    assert isinstance(form.test_field, IntegerFieldWithSeparator)
    assert form.test_field.label.text == answer_schema["label"]
    assert form.test_field.description == answer_schema["guidance"]


def test_decimal_field(value_source_resolver, rule_evaluator):
    answer_schema = {
        "guidance": "",
        "id": "lightsaber-cost-answer",
        "label": "How hot is a lightsaber in degrees C?",
        "mandatory": False,
        "type": "Number",
        "decimal_places": 2,
        "validation": {
            "messages": {
                "INVALID_NUMBER": "Please only enter whole numbers into the field."
            }
        },
    }

    form_class = get_test_form_class(
        answer_schema, value_source_resolver, rule_evaluator, error_messages
    )
    form = form_class()

    assert isinstance(form.test_field, DecimalFieldWithSeparator)
    assert form.test_field.label.text == answer_schema["label"]
    assert form.test_field.description == answer_schema["guidance"]


def test_currency_field(value_source_resolver, rule_evaluator):
    answer_schema = {
        "guidance": "",
        "id": "a04a516d-502d-4068-bbed-a43427c68cd9",
        "mandatory": False,
        "label": "",
        "type": "Currency",
        "validation": {
            "messages": {
                "INVALID_NUMBER": "Please only enter whole numbers into the field."
            }
        },
    }

    form_class = get_test_form_class(
        answer_schema, value_source_resolver, rule_evaluator, error_messages
    )
    form = form_class()

    assert isinstance(form.test_field, IntegerFieldWithSeparator)
    assert form.test_field.label.text == answer_schema["label"]
    assert form.test_field.description == answer_schema["guidance"]


def test_percentage_field(value_source_resolver, rule_evaluator):
    answer_schema = {
        "description": "",
        "id": "percentage-turnover-2016-market-new-answer",
        "label": "New to the market in 2014-2016",
        "mandatory": False,
        "q_code": "0810",
        "type": "Percentage",
        "maximum": {"value": 100},
        "validation": {
            "messages": {
                "NUMBER_TOO_LARGE": "How much, fool you must be",
                "NUMBER_TOO_SMALL": "How can it be negative?",
                "INVALID_NUMBER": "Please only enter whole numbers into the field.",
            }
        },
    }

    form_class = get_test_form_class(
        answer_schema, value_source_resolver, rule_evaluator, error_messages
    )
    form = form_class()

    assert isinstance(form.test_field, IntegerFieldWithSeparator)
    assert form.test_field.label.text == answer_schema["label"]
    assert form.test_field.description == answer_schema["description"]


def test_manual_min(app, value_source_resolver, rule_evaluator):
    answer_schema = {
        "minimum": {"value": 10},
        "label": "Min Test",
        "mandatory": False,
        "validation": {
            "messages": {
                "INVALID_NUMBER": "Please only enter whole numbers into the field.",
                "NUMBER_TOO_SMALL": "The minimum value allowed is 10. Please correct your answer.",
            }
        },
        "id": "test-range",
        "type": "Currency",
    }

    test_form_class = get_test_form_class(
        answer_schema, value_source_resolver, rule_evaluator, error_messages
    )
    form = test_form_class(MultiDict({"test_field": "9"}))

    form.validate()

    assert (
        form.errors["test_field"][0]
        == answer_schema["validation"]["messages"]["NUMBER_TOO_SMALL"]
    )


def test_manual_max(app, value_source_resolver, rule_evaluator):
    answer_schema = {
        "maximum": {"value": 20},
        "label": "Max Test",
        "mandatory": False,
        "validation": {
            "messages": {
                "INVALID_NUMBER": "Please only enter whole numbers into the field.",
                "NUMBER_TOO_LARGE": "The maximum value allowed is 20. Please correct your answer.",
            }
        },
        "id": "test-range",
        "type": "Currency",
    }

    test_form_class = get_test_form_class(
        answer_schema, value_source_resolver, rule_evaluator
    )
    form = test_form_class(MultiDict({"test_field": "21"}))

    form.validate()

    assert (
        form.errors["test_field"][0]
        == answer_schema["validation"]["messages"]["NUMBER_TOO_LARGE"]
    )


def test_manual_decimal(app, value_source_resolver, rule_evaluator):
    answer_schema = {
        "decimal_places": 2,
        "label": "Range Test 10 to 20",
        "mandatory": False,
        "validation": {
            "messages": {
                "INVALID_NUMBER": "Please only enter whole numbers into the field.",
                "INVALID_DECIMAL": "Please enter a number to 2 decimal places.",
            }
        },
        "id": "test-range",
        "type": "Currency",
    }

    test_form_class = get_test_form_class(
        answer_schema, value_source_resolver, rule_evaluator
    )
    form = test_form_class(MultiDict({"test_field": "1.234"}))
    form.validate()

    assert (
        form.errors["test_field"][0]
        == answer_schema["validation"]["messages"]["INVALID_DECIMAL"]
    )


def test_zero_max(app, value_source_resolver, rule_evaluator):
    maximum = 0

    answer_schema = {
        "maximum": {"value": maximum},
        "label": "Max Test",
        "mandatory": False,
        "id": "test-range",
        "type": "Currency",
    }
    error_message = error_messages["NUMBER_TOO_LARGE"] % {"max": maximum}
    test_form_class = get_test_form_class(
        answer_schema, value_source_resolver, rule_evaluator, messages=error_messages
    )
    form = test_form_class(MultiDict({"test_field": "1"}))
    form.validate()

    assert form.errors["test_field"][0] == error_message


def test_zero_min(app, value_source_resolver, rule_evaluator):
    minimum = 0

    answer_schema = {
        "maximum": {"value": minimum},
        "label": "Max Test",
        "mandatory": False,
        "id": "test-range",
        "type": "Currency",
    }
    error_message = error_messages["NUMBER_TOO_SMALL"] % {"min": minimum}
    test_form_class = get_test_form_class(
        answer_schema, value_source_resolver, rule_evaluator, error_messages
    )
    form = test_form_class(MultiDict({"test_field": "-1"}))
    form.validate()

    assert form.errors["test_field"][0] == error_message


def test_value_min_and_max(app, value_source_resolver, rule_evaluator):
    answer_schema = {
        "minimum": {"value": 10},
        "maximum": {"value": 20},
        "label": "Range Test 10 to 20",
        "mandatory": False,
        "validation": {
            "messages": {
                "INVALID_NUMBER": "Please only enter whole numbers into the field.",
                "NUMBER_TOO_SMALL": "The minimum value allowed is 10. Please correct your answer.",
                "NUMBER_TOO_LARGE": "The maximum value allowed is 20. Please correct your answer.",
            }
        },
        "id": "test-range",
        "type": "Currency",
    }

    test_form_class = get_test_form_class(
        answer_schema, value_source_resolver, rule_evaluator
    )
    form = test_form_class(MultiDict({"test_field": "9"}))
    form.validate()

    assert (
        form.errors["test_field"][0]
        == answer_schema["validation"]["messages"]["NUMBER_TOO_SMALL"]
    )

    form = test_form_class(MultiDict({"test_field": "22"}))
    form.validate()

    assert (
        form.errors["test_field"][0]
        == answer_schema["validation"]["messages"]["NUMBER_TOO_LARGE"]
    )


def test_manual_min_exclusive(app, value_source_resolver, rule_evaluator):
    answer_schema = {
        "minimum": {"value": 10, "exclusive": True},
        "label": "Min Test",
        "mandatory": False,
        "validation": {
            "messages": {
                "INVALID_NUMBER": "Please only enter whole numbers into the field.",
                "NUMBER_TOO_SMALL_EXCLUSIVE": "The minimum value allowed is 10. Please correct your answer.",
            }
        },
        "id": "test-range",
        "type": "Currency",
    }

    test_form_class = get_test_form_class(
        answer_schema, value_source_resolver, rule_evaluator
    )

    form = test_form_class(MultiDict({"test_field": "10"}))
    form.validate()

    assert (
        form.errors["test_field"][0]
        == answer_schema["validation"]["messages"]["NUMBER_TOO_SMALL_EXCLUSIVE"]
    )


def test_manual_max_exclusive(app, value_source_resolver, rule_evaluator):
    answer_schema = {
        "maximum": {"value": 20, "exclusive": True},
        "label": "Max Test",
        "mandatory": False,
        "validation": {
            "messages": {
                "INVALID_NUMBER": "Please only enter whole numbers into the field.",
                "NUMBER_TOO_LARGE_EXCLUSIVE": "The maximum value allowed is 20. Please correct your answer.",
            }
        },
        "id": "test-range",
        "type": "Currency",
    }

    test_form_class = get_test_form_class(
        answer_schema, value_source_resolver, rule_evaluator
    )

    form = test_form_class(MultiDict({"test_field": "20"}))
    form.validate()

    assert (
        form.errors["test_field"][0]
        == answer_schema["validation"]["messages"]["NUMBER_TOO_LARGE_EXCLUSIVE"]
    )


def test_default_range(value_source_resolver, rule_evaluator):
    answer = {
        "decimal_places": 2,
        "label": "Range Test 10 to 20",
        "mandatory": False,
        "validation": {
            "messages": {
                "INVALID_NUMBER": "Please only enter whole numbers into the field.",
                "NUMBER_TOO_SMALL": "The minimum value allowed is 10. Please correct your answer.",
                "NUMBER_TOO_LARGE": "The maximum value allowed is 20. Please correct your answer.",
            }
        },
        "id": "test-range",
        "type": "Currency",
    }
    handler = NumberHandler(
        answer, value_source_resolver, rule_evaluator, error_messages
    )
    field_references = handler.references

    assert field_references["maximum"] == MAX_NUMBER
    assert field_references["minimum"] == 0


def test_get_schema_value_answer_store(value_source_resolver, rule_evaluator):
    answer_schema = {
        "id": "test-range",
        "label": "",
        "description": "Range Test",
        "mandatory": False,
        "type": "Number",
        "decimal_places": 2,
        "maximum": {"value": {"identifier": "set-maximum", "source": "answers"}},
        "minimum": {"value": {"identifier": "set-minimum", "source": "answers"}},
    }
    value_source_resolver.metadata = {
        "schema_name": "test_numbers",
        "language_code": "en",
    }
    answer_store = AnswerStore()

    answer_store.add_or_update(Answer(answer_id="set-maximum", value=10))
    answer_store.add_or_update(Answer(answer_id="set-minimum", value=1))
    value_source_resolver.answer_store = answer_store
    number_handler = NumberHandler(
        answer_schema, value_source_resolver, rule_evaluator, error_messages
    )

    maximum = number_handler.get_schema_value(answer_schema["maximum"])
    minimum = number_handler.get_schema_value(answer_schema["minimum"])

    assert maximum == 10
    assert minimum == 1
