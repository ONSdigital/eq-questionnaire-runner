# coding: utf-8
from unittest.mock import MagicMock, patch

from jinja2 import Undefined
from mock import Mock

from app.jinja_filters import (
    CheckboxConfig,
    RadioConfig,
    format_datetime,
    format_duration,
    format_number,
    format_percentage,
    format_unit,
    format_unit_input_label,
    get_currency_symbol,
    get_formatted_address,
    get_formatted_currency,
    get_width_class_for_number,
    map_list_collector_config,
)
from tests.app.app_context_test_case import AppContextTestCase


class TestJinjaFilters(AppContextTestCase):  # pylint: disable=too-many-public-methods
    def setUp(self):
        self.autoescape_context = Mock(autoescape=True)
        super(TestJinjaFilters, self).setUp()

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
        # Given a date after DST started
        date_time = "2018-03-29T11:59:13.528680"

        # When
        with self.app_request_context("/"):
            format_value = format_datetime(self.autoescape_context, date_time)

        # Then
        self.assertEqual(
            format_value, "<span class='date'>29 March 2018 at 12:59</span>"
        )

    def test_format_date_time_in_gmt(self):
        # Given
        date_time = "2018-10-28T11:59:13.528680"

        # When
        with self.app_request_context("/"):
            format_value = format_datetime(self.autoescape_context, date_time)

        # Then
        self.assertEqual(
            format_value, "<span class='date'>28 October 2018 at 11:59</span>"
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
    def test_format_unit_input_label(self):
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
        self.assertEqual(format_unit_input_label("duration-hour", "long"), "hours")
        self.assertEqual(format_unit_input_label("duration-year"), "yr")
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

    def test_get_width_class_for_number_no_maximum(self):
        self.assertEqual(get_width_class_for_number({}), "input--w-10")

    def test_get_width_class_for_number_single_digit(self):
        answer = {"maximum": {"value": 1}}
        self.assertEqual(get_width_class_for_number(answer), "input--w-1")

    def test_get_width_class_for_number_multiple_digits(self):
        answer = {"maximum": {"value": 123456}}
        self.assertEqual(get_width_class_for_number(answer), "input--w-6")

    def test_get_width_class_for_number_roundup(self):
        answer = {"maximum": {"value": 12345678901}}
        self.assertEqual(get_width_class_for_number(answer), "input--w-20")

    def test_get_width_class_for_number_min_value_longer_than_maximum(self):
        answer = {"minimum": {"value": -123456}, "maximum": {"value": 1234}}
        self.assertEqual(get_width_class_for_number(answer), "input--w-7")

    def test_get_width_class_for_number_decimal_places(self):
        answer = {"decimal_places": 2, "maximum": {"value": 123456}}
        self.assertEqual(get_width_class_for_number(answer), "input--w-8")

    def test_get_width_class_for_number_large_number(self):
        answer = {"maximum": {"value": 123456789012345678901}}
        self.assertIsNone(get_width_class_for_number(answer))

    @staticmethod
    def test_radio_class_visible_attribute():
        answer = {
            "type": "Radio",
            "id": "radio-answer-numeric-detail",
            "mandatory": False,
            "options": [
                {
                    "label": "Other",
                    "value": "Other",
                    "detail_answer": {
                        "mandatory": False,
                        "id": "other-answer",
                        "label": "Please enter a number of items",
                        "type": "Number",
                        "parent_id": "radio-question-numeric-detail",
                        "visible": True,
                    },
                }
            ],
            "parent_id": "radio-question-numeric-detail",
        }

        option = Mock()
        option.detail_answer_id = "other-answer"
        radio = RadioConfig(option=option, index=0, form=MagicMock(), answer=answer)

        assert radio.other.open is True

    @staticmethod
    def test_checkbox_detail_answer_visible_attribute():
        answer = {
            "type": "Checkbox",
            "id": "checkbox-answer-numeric-detail",
            "mandatory": False,
            "options": [
                {
                    "label": "Other",
                    "value": "Other",
                    "detail_answer": {
                        "mandatory": False,
                        "id": "other-answer",
                        "label": "Please enter a number of items",
                        "type": "Number",
                        "parent_id": "checkbox-question-numeric-detail",
                        "visible": True,
                    },
                }
            ],
            "parent_id": "checkbox-question-numeric-detail",
        }

        option = Mock()
        option.detail_answer_id = "other-answer"
        checkbox = CheckboxConfig(
            option=option, index=0, form=MagicMock(), answer=answer
        )

        assert checkbox.other.open is True

    @staticmethod
    def test_checkbox_mutually_exclusive_detail_answer_visible_attribute():
        answer = {
            "type": "MutuallyExclusive",
            "id": "answer-numeric-detail-exclusive",
            "mandatory": False,
            "options": [
                {
                    "label": "Other",
                    "value": "Other",
                    "detail_answer": {
                        "mandatory": False,
                        "id": "other-answer",
                        "label": "Please enter a number of items",
                        "type": "Number",
                        "parent_id": "checkbox-question-numeric-exclusive",
                        "visible": True,
                    },
                }
            ],
            "parent_id": "question-numeric-detail-exclusive",
        }

        option = Mock()
        option.detail_answer_id = "other-answer"
        checkbox = CheckboxConfig(
            option=option, index=0, form=MagicMock(), answer=answer
        )

        assert checkbox.other.open is True

    @staticmethod
    def test_radio_class_detail_answer_display_width_with_max_value():
        answer = {
            "type": "Radio",
            "id": "radio-answer-numeric-detail",
            "mandatory": False,
            "options": [
                {
                    "label": "Other",
                    "value": "Other",
                    "detail_answer": {
                        "mandatory": False,
                        "id": "other-answer",
                        "label": "Please enter a number of items",
                        "type": "Number",
                        "maximum": {"value": 20},
                        "parent_id": "radio-question-numeric-detail",
                        "visible": False,
                    },
                }
            ],
            "parent_id": "radio-question-numeric-detail",
        }

        option = Mock()
        option.detail_answer_id = "other-answer"
        radio = RadioConfig(option=option, index=0, form=MagicMock(), answer=answer)

        assert radio.other.classes == "input--w-2"


def test_map_list_collector_config_no_actions():
    list_items = [{"item_title": "Mark Bloggs"}, {"item_title": "Joe Bloggs"}]

    output = map_list_collector_config(list_items, "icon")

    expected = [
        {
            "rowItems": [
                {
                    "actions": [],
                    "icon": "icon",
                    "rowTitle": "Mark Bloggs",
                    "rowTitleAttributes": {"data-qa": "list-item-1-label"},
                }
            ]
        },
        {
            "rowItems": [
                {
                    "actions": [],
                    "icon": "icon",
                    "rowTitle": "Joe Bloggs",
                    "rowTitleAttributes": {"data-qa": "list-item-2-label"},
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
        },
        {
            "remove_link": "/nonprimary/remove",
            "edit_link": "/nonprimary/change",
            "primary_person": False,
            "item_title": "Joe Bloggs",
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
                    "icon": "icon",
                    "rowTitle": "Mark Bloggs (You)",
                    "rowTitleAttributes": {"data-qa": "list-item-1-label"},
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
                    "icon": "icon",
                    "rowTitle": "Joe Bloggs",
                    "rowTitleAttributes": {"data-qa": "list-item-2-label"},
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
