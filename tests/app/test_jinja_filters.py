# coding: utf-8
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import pytest
import simplejson as json
from jinja2 import Undefined
from mock import Mock

from app.jinja_filters import (
    OtherConfig,
    SummaryRow,
    format_datetime,
    format_duration,
    format_number,
    format_percentage,
    format_unit,
    format_unit_input_label,
    get_currency_symbol,
    get_formatted_address,
    get_formatted_currency,
    get_width_for_number,
    map_list_collector_config,
    map_summary_item_config,
    should_wrap_with_fieldset,
    strip_tags,
)
from tests.app.app_context_test_case import AppContextTestCase


class TestJinjaFilters(AppContextTestCase):  # pylint: disable=too-many-public-methods
    def setUp(self):
        self.autoescape_context = Mock(autoescape=True)
        super().setUp()

    def test_strip_tags(self):
        self.assertEqual(strip_tags("Hello <b>world</b>"), "Hello world")
        self.assertEqual(
            strip_tags("Hello &lt;i&gt;world&lt;/i&gt;"),
            "Hello &lt;i&gt;world&lt;/i&gt;",
        )
        self.assertEqual(
            strip_tags("Hello <b>&lt;i&gt;world&lt;/i&gt;</b>"),
            "Hello &lt;i&gt;world&lt;/i&gt;",
        )

    @patch("app.jinja_filters.flask_babel.get_locale", Mock(return_value="en_GB"))
    def test_get_currency_symbol(self):
        self.assertEqual(get_currency_symbol("GBP"), "£")
        self.assertEqual(get_currency_symbol("EUR"), "€")
        self.assertEqual(get_currency_symbol("USD"), "US$")
        self.assertEqual(get_currency_symbol("JPY"), "JP¥")
        self.assertEqual(get_currency_symbol(""), "")

    @patch("app.jinja_filters.flask_babel.get_locale", Mock(return_value="en_GB"))
    def test_format_number(self):
        self.assertEqual(format_number(123), "123")
        self.assertEqual(format_number("123.4"), "123.4")
        self.assertEqual(format_number("123.40"), "123.4")
        self.assertEqual(format_number("1000"), "1,000")
        self.assertEqual(format_number("10000"), "10,000")
        self.assertEqual(format_number("100000000"), "100,000,000")
        self.assertEqual(format_number(0), "0")
        self.assertEqual(format_number(0.00), "0")
        self.assertEqual(format_number(""), "")
        self.assertEqual(format_number(None), "")
        self.assertEqual(format_number(Undefined()), "")

    def test_format_date_time_in_bst(self):
        # Given a date after BST started
        date_time = datetime(2018, 3, 29, 23, 59, 0, tzinfo=timezone.utc)

        # When
        with self.app_request_context("/"):
            format_value = format_datetime(self.autoescape_context, date_time)

        # Then
        self.assertEqual(
            format_value, "<span class='date'>30 March 2018 at 00:59</span>"
        )

    def test_format_date_time_in_gmt(self):
        # Given
        test_data = {
            datetime(
                2018, 10, 28, 00, 15, 0, tzinfo=timezone.utc
            ): "28 October 2018 at 01:15",
            # Clocks go back on 29th Oct 2018
            datetime(
                2018, 10, 29, 00, 15, 0, tzinfo=timezone.utc
            ): "29 October 2018 at 00:15",
        }
        for date_time, expected_value in test_data.items():
            with self.subTest(
                date_time=date_time,
                expected_value=expected_value,
            ):
                date_time = date_time.replace(tzinfo=timezone.utc)
                # When
                with self.app_request_context("/"):
                    format_value = format_datetime(self.autoescape_context, date_time)

                # Then
                self.assertEqual(
                    format_value, f"<span class='date'>{expected_value}</span>"
                )

    def test_format_percentage(self):
        self.assertEqual(format_percentage("100"), "100%")
        self.assertEqual(format_percentage(100), "100%")
        self.assertEqual(format_percentage(4.5), "4.5%")

    @patch("app.jinja_filters.flask_babel.get_locale", Mock(return_value="en_GB"))
    def test_format_unit(self):
        self.assertEqual(format_unit("length-meter", 100), "100 m")
        self.assertEqual(format_unit("length-centimeter", 100), "100 cm")
        self.assertEqual(format_unit("length-mile", 100), "100 mi")
        self.assertEqual(format_unit("length-kilometer", 100), "100 km")
        self.assertEqual(format_unit("area-square-meter", 100), "100 m²")
        self.assertEqual(format_unit("area-square-centimeter", 100), "100 cm²")
        self.assertEqual(format_unit("area-square-kilometer", 100), "100 km²")
        self.assertEqual(format_unit("area-square-mile", 100), "100 sq mi")
        self.assertEqual(format_unit("area-hectare", 100), "100 ha")
        self.assertEqual(format_unit("area-acre", 100), "100 ac")
        self.assertEqual(format_unit("volume-cubic-meter", 100), "100 m³")
        self.assertEqual(format_unit("volume-cubic-centimeter", 100), "100 cm³")
        self.assertEqual(format_unit("volume-liter", 100), "100 l")
        self.assertEqual(format_unit("volume-hectoliter", 100), "100 hl")
        self.assertEqual(format_unit("volume-megaliter", 100), "100 Ml")
        self.assertEqual(format_unit("duration-hour", 100), "100 hrs")
        self.assertEqual(format_unit("duration-hour", 100, "long"), "100 hours")
        self.assertEqual(format_unit("duration-year", 100, "long"), "100 years")

    @patch("app.jinja_filters.flask_babel.get_locale", Mock(return_value="cy"))
    def test_format_unit_welsh(self):
        self.assertEqual(format_unit("duration-hour", 100), "100 awr")
        self.assertEqual(format_unit("duration-year", 100), "100 bl")
        self.assertEqual(format_unit("duration-hour", 100, "long"), "100 awr")
        self.assertEqual(format_unit("duration-year", 100, "long"), "100 mlynedd")

    @patch("app.jinja_filters.flask_babel.get_locale", Mock(return_value="en_GB"))
    def test_format_unit_input_label_short(self):
        self.assertEqual(format_unit_input_label("length-meter"), "m")
        self.assertEqual(format_unit_input_label("length-centimeter"), "cm")
        self.assertEqual(format_unit_input_label("length-mile"), "mi")
        self.assertEqual(format_unit_input_label("length-kilometer"), "km")
        self.assertEqual(format_unit_input_label("area-square-meter"), "m²")
        self.assertEqual(format_unit_input_label("area-square-centimeter"), "cm²")
        self.assertEqual(format_unit_input_label("area-square-kilometer"), "km²")
        self.assertEqual(format_unit_input_label("area-square-mile"), "sq mi")
        self.assertEqual(format_unit_input_label("area-hectare"), "ha")
        self.assertEqual(format_unit_input_label("area-acre"), "ac")
        self.assertEqual(format_unit_input_label("volume-cubic-meter"), "m³")
        self.assertEqual(format_unit_input_label("volume-cubic-centimeter"), "cm³")
        self.assertEqual(format_unit_input_label("volume-liter"), "l")
        self.assertEqual(format_unit_input_label("volume-hectoliter"), "hl")
        self.assertEqual(format_unit_input_label("volume-megaliter"), "Ml")
        self.assertEqual(format_unit_input_label("duration-hour"), "hr")
        self.assertEqual(format_unit_input_label("duration-year"), "yr")

    @patch("app.jinja_filters.flask_babel.get_locale", Mock(return_value="en_GB"))
    def test_format_unit_input_label_long(self):
        self.assertEqual(format_unit_input_label("length-meter", "long"), "metres")
        self.assertEqual(
            format_unit_input_label("length-centimeter", "long"), "centimetres"
        )
        self.assertEqual(format_unit_input_label("length-mile", "long"), "miles")
        self.assertEqual(
            format_unit_input_label("length-kilometer", "long"), "kilometres"
        )
        self.assertEqual(
            format_unit_input_label("area-square-meter", "long"), "square metres"
        )
        self.assertEqual(
            format_unit_input_label("area-square-centimeter", "long"),
            "square centimetres",
        )
        self.assertEqual(
            format_unit_input_label("area-square-kilometer", "long"),
            "square kilometres",
        )
        self.assertEqual(
            format_unit_input_label("area-square-mile", "long"), "square miles"
        )
        self.assertEqual(format_unit_input_label("area-hectare", "long"), "hectares")
        self.assertEqual(format_unit_input_label("area-acre", "long"), "acres")
        self.assertEqual(
            format_unit_input_label("volume-cubic-meter", "long"), "cubic metres"
        )
        self.assertEqual(
            format_unit_input_label("volume-cubic-centimeter", "long"),
            "cubic centimetres",
        )
        self.assertEqual(format_unit_input_label("volume-liter", "long"), "litres")
        self.assertEqual(
            format_unit_input_label("volume-hectoliter", "long"), "hectolitres"
        )
        self.assertEqual(
            format_unit_input_label("volume-megaliter", "long"), "megalitres"
        )
        self.assertEqual(format_unit_input_label("duration-hour", "long"), "hours")
        self.assertEqual(format_unit_input_label("duration-year", "long"), "years")

    @patch("app.jinja_filters.flask_babel.get_locale", Mock(return_value="cy"))
    def test_format_unit_input_label_welsh(self):
        self.assertEqual(format_unit_input_label("duration-hour"), "awr")
        self.assertEqual(format_unit_input_label("duration-hour", "long"), "awr")
        self.assertEqual(format_unit_input_label("duration-year"), "bl")
        self.assertEqual(format_unit_input_label("duration-year", "long"), "flynedd")

    def test_format_year_month_duration(self):
        with self.app_request_context("/"):
            self.assertEqual(
                format_duration({"years": 5, "months": 4}), "5 years 4 months"
            )
            self.assertEqual(format_duration({"years": 5, "months": 0}), "5 years")
            self.assertEqual(format_duration({"years": 0, "months": 4}), "4 months")
            self.assertEqual(
                format_duration({"years": 1, "months": 1}), "1 year 1 month"
            )
            self.assertEqual(format_duration({"years": 0, "months": 0}), "0 months")

    def test_format_year_duration(self):
        with self.app_request_context("/"):
            self.assertEqual(format_duration({"years": 5}), "5 years")
            self.assertEqual(format_duration({"years": 1}), "1 year")
            self.assertEqual(format_duration({"years": 0}), "0 years")

    def test_format_month_duration(self):
        with self.app_request_context("/"):
            self.assertEqual(format_duration({"months": 5}), "5 months")
            self.assertEqual(format_duration({"months": 1}), "1 month")
            self.assertEqual(format_duration({"months": 0}), "0 months")

    def test_get_formatted_currency_with_no_value(self):
        self.assertEqual(get_formatted_currency(""), "")

    def test_get_width_for_number_no_maximum(self):
        self.assertEqual(get_width_for_number({}), 10)

    def test_get_width_for_number_single_digit(self):
        answer = {"maximum": {"value": 1}}
        self.assertEqual(get_width_for_number(answer), 1)

    def test_get_width_for_number_multiple_digits(self):
        answer = {"maximum": {"value": 123456}}
        self.assertEqual(get_width_for_number(answer), 6)

    def test_get_width_for_number_roundup(self):
        answer = {"maximum": {"value": 12345678901}}
        self.assertEqual(get_width_for_number(answer), 15)

    def test_get_width_for_number_min_value_longer_than_maximum(self):
        answer = {"minimum": {"value": -123456}, "maximum": {"value": 1234}}
        self.assertEqual(get_width_for_number(answer), 7)

    def test_get_width_for_number_decimal_places(self):
        answer = {"decimal_places": 2, "maximum": {"value": 123456}}
        self.assertEqual(get_width_for_number(answer), 8)

    def test_get_width_for_number_large_number(self):
        answer = {
            "maximum": {"value": 123456789012345678901123456789012345678901234567890}
        }
        self.assertIsNone(get_width_for_number(answer))

    def test_should_wrap_with_fieldset_daterange(self):
        question = {"type": "DateRange"}
        self.assertFalse(should_wrap_with_fieldset(question))

    def test_should_wrap_with_fieldset_mutually_exclusive(self):
        question = {"type": "MutuallyExclusive", "answers": []}
        self.assertTrue(should_wrap_with_fieldset(question))

    def test_should_wrap_with_fieldset_multiple_answers(self):
        question = {
            "type": "General",
            "answers": [{"type": "TextField"}, {"type": "TextField"}],
        }
        self.assertTrue(should_wrap_with_fieldset(question))

    def test_should_wrap_with_fieldset_single_answer(self):
        for answer_type in [
            "Radio",
            "Date",
            "MonthYearDate",
            "Duration",
            "Address",
            "Relationship",
            "Checkbox",
        ]:
            question = {"type": "General", "answers": [{"type": answer_type}]}
            self.assertTrue(should_wrap_with_fieldset(question))

    def test_should_wrap_with_fieldset_single_answer_with_label(self):
        for answer_type in [
            "Radio",
            "Date",
            "MonthYearDate",
            "Duration",
            "Address",
            "Relationship",
            "Checkbox",
        ]:
            question = {
                "type": "General",
                "answers": [{"type": answer_type, "label": "Label"}],
            }
            self.assertFalse(should_wrap_with_fieldset(question))


def test_map_list_collector_config_no_actions():
    list_items = [
        {"item_title": "Mark Bloggs", "list_item_id": "one"},
        {"item_title": "Joe Bloggs", "list_item_id": "two"},
    ]

    output = map_list_collector_config(list_items, "icon")

    expected = [
        {
            "rowItems": [
                {
                    "actions": [],
                    "iconType": "icon",
                    "rowTitle": "Mark Bloggs",
                    "rowTitleAttributes": {
                        "data-qa": "list-item-1-label",
                        "data-list-item-id": "one",
                    },
                }
            ]
        },
        {
            "rowItems": [
                {
                    "actions": [],
                    "iconType": "icon",
                    "rowTitle": "Joe Bloggs",
                    "rowTitleAttributes": {
                        "data-qa": "list-item-2-label",
                        "data-list-item-id": "two",
                    },
                }
            ]
        },
    ]

    assert output == expected


def test_map_list_collector_config():
    list_items = [
        {
            "remove_link": "/primary/remove",
            "edit_link": "/primary/change",
            "primary_person": True,
            "item_title": "Mark Bloggs (You)",
            "list_item_id": "primary",
        },
        {
            "remove_link": "/nonprimary/remove",
            "edit_link": "/nonprimary/change",
            "primary_person": False,
            "item_title": "Joe Bloggs",
            "list_item_id": "nonprimary",
        },
    ]

    output = map_list_collector_config(
        list_items,
        "icon",
        "edit_link_text",
        "edit_link_aria_label",
        "remove_link_text",
        "remove_link_aria_label",
    )

    expected = [
        {
            "rowItems": [
                {
                    "actions": [
                        {
                            "ariaLabel": "edit_link_aria_label",
                            "attributes": {"data-qa": "list-item-change-1-link"},
                            "text": "edit_link_text",
                            "url": "/primary/change",
                        }
                    ],
                    "iconType": "icon",
                    "rowTitle": "Mark Bloggs (You)",
                    "rowTitleAttributes": {
                        "data-qa": "list-item-1-label",
                        "data-list-item-id": "primary",
                    },
                }
            ]
        },
        {
            "rowItems": [
                {
                    "actions": [
                        {
                            "ariaLabel": "edit_link_aria_label",
                            "attributes": {"data-qa": "list-item-change-2-link"},
                            "text": "edit_link_text",
                            "url": "/nonprimary/change",
                        },
                        {
                            "ariaLabel": "remove_link_aria_label",
                            "attributes": {"data-qa": "list-item-remove-2-link"},
                            "text": "remove_link_text",
                            "url": "/nonprimary/remove",
                        },
                    ],
                    "iconType": "icon",
                    "rowTitle": "Joe Bloggs",
                    "rowTitleAttributes": {
                        "data-qa": "list-item-2-label",
                        "data-list-item-id": "nonprimary",
                    },
                }
            ]
        },
    ]

    assert output == expected


def test_format_address_fields():
    address_fields = {
        "line": "7 Evelyn Street",
        "town": "Barry",
        "postcode": "CF63 4JG",
    }

    assert (
        get_formatted_address(address_fields) == "7 Evelyn Street<br>Barry<br>CF63 4JG"
    )


def test_format_address_fields_with_uprn():
    address_fields = {
        "line": "7 Evelyn Street",
        "town": "Barry",
        "postcode": "CF63 4JG",
        "uprn": "64037876",
    }

    assert (
        get_formatted_address(address_fields) == "7 Evelyn Street<br>Barry<br>CF63 4JG"
    )


@pytest.mark.parametrize(
    "max_value, expected_width",
    [
        (None, 10),
        (1, 1),
        (123123123123, 15),
    ],
)
def test_other_config_numeric_input_class(
    answer_schema_number, max_value, expected_width
):
    if max_value:
        answer_schema_number["maximum"] = {"value": max_value}

    other = OtherConfig(Mock(), answer_schema_number)
    assert other.width == expected_width


def test_other_config_non_dropdown_input_type(answer_schema_textfield):
    other = OtherConfig(Mock(), answer_schema_textfield)
    assert other.otherType == "input"


def test_other_config_dropdown_input_type(answer_schema_dropdown):
    other = OtherConfig(MagicMock(), answer_schema_dropdown)
    assert other.otherType == "select"


def test_other_config_dropdown_has_options_attribute(answer_schema_dropdown):
    other = OtherConfig(MagicMock(), answer_schema_dropdown)
    assert hasattr(other, "options")
    assert not hasattr(other, "value")


def test_other_config_non_dropdown_has_value_attribute(answer_schema_textfield):
    other = OtherConfig(MagicMock(), answer_schema_textfield)
    assert hasattr(other, "value")
    assert not hasattr(other, "options")


@pytest.mark.parametrize(
    "is_visible, expected_visibility",
    [
        (True, True),
        (False, False),
        (None, False),
    ],
)
def test_other_config_visibility(
    answer_schema_textfield, is_visible, expected_visibility
):
    if is_visible is not None:
        answer_schema_textfield["visible"] = is_visible

    other = OtherConfig(Mock(), answer_schema_textfield)
    assert other.open is expected_visibility


@patch("app.jinja_filters.flask_babel.get_locale", Mock(return_value="en_GB"))
def test_calculated_summary_config():
    expected = [
        SummaryRow(
            block={
                "id": "first-number-block",
                "link": "/questionnaire/first-number-block/?return_to=final-summary",
                "question": {
                    "id": "first-number-question",
                    "type": "General",
                    "title": "First Number Question Title",
                    "answers": [
                        {
                            "id": "first-number-answer",
                            "label": "First answer label",
                            "value": 1,
                            "type": "currency",
                            "currency": "GBP",
                        }
                    ],
                },
            },
            question={
                "id": "first-number-question",
                "type": "General",
                "title": "First Number Question Title",
                "answers": [
                    {
                        "id": "first-number-answer",
                        "label": "First answer label",
                        "value": 1,
                        "type": "currency",
                        "currency": "GBP",
                    }
                ],
            },
            summary_type="CalculatedSummary",
            answers_are_editable=True,
            no_answer_provided="No answer Provided",
            edit_link_text="Change",
            edit_link_aria_label="Change your answer for",
        ),
        SummaryRow(
            block={
                "id": "second-number-block",
                "link": "/questionnaire/second-number-block/?return_to=final-summary",
                "question": {
                    "id": "second-number-question",
                    "type": "General",
                    "title": "Second Number Question Title",
                    "answers": [
                        {
                            "id": "second-number-answer",
                            "label": "Second answer label",
                            "value": 1,
                            "type": "currency",
                            "currency": "GBP",
                        }
                    ],
                },
            },
            question={
                "id": "second-number-question",
                "type": "General",
                "title": "Second Number Question Title",
                "answers": [
                    {
                        "id": "second-number-answer",
                        "label": "Second answer label",
                        "value": 1,
                        "type": "currency",
                        "currency": "GBP",
                    }
                ],
            },
            summary_type="CalculatedSummary",
            answers_are_editable=True,
            no_answer_provided="No answer Provided",
            edit_link_text="Change",
            edit_link_aria_label="Change your answer for",
        ),
        SummaryRow(
            block=None,
            question={
                "title": "Grand total of previous values",
                "id": "calculated-summary-question",
                "answers": [{"id": "calculated-summary-answer", "value": "£2.00"}],
            },
            summary_type="CalculatedSummary",
            answers_are_editable=False,
            no_answer_provided=None,
            edit_link_text=None,
            edit_link_aria_label=None,
        ),
    ]

    result = map_summary_item_config(
        group={
            "blocks": [
                {
                    "id": "first-number-block",
                    "link": "/questionnaire/first-number-block/?return_to=final-summary",
                    "question": {
                        "id": "first-number-question",
                        "type": "General",
                        "title": "First Number Question Title",
                        "answers": [
                            {
                                "id": "first-number-answer",
                                "label": "First answer label",
                                "value": 1,
                                "type": "currency",
                                "currency": "GBP",
                            }
                        ],
                    },
                },
                {
                    "id": "second-number-block",
                    "link": "/questionnaire/second-number-block/?return_to=final-summary",
                    "question": {
                        "id": "second-number-question",
                        "type": "General",
                        "title": "Second Number Question Title",
                        "answers": [
                            {
                                "id": "second-number-answer",
                                "label": "Second answer label",
                                "value": 1,
                                "type": "currency",
                                "currency": "GBP",
                            }
                        ],
                    },
                },
            ],
        },
        summary_type="CalculatedSummary",
        answers_are_editable=True,
        no_answer_provided="No answer Provided",
        edit_link_text="Change",
        edit_link_aria_label="Change your answer for",
        calculated_question={
            "title": "Grand total of previous values",
            "id": "calculated-summary-question",
            "answers": [{"id": "calculated-summary-answer", "value": "£2.00"}],
        },
    )

    assert to_dict(expected) == to_dict(result)


def to_dict(obj):
    return json.loads(json.dumps(obj, default=lambda o: o.__dict__))
