# coding: utf-8
from datetime import datetime, timezone

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


@pytest.mark.parametrize(
    "tagged_string, expected",
    (
        ("Hello <b>world</b>", "Hello world"),
        ("Hello &lt;i&gt;world&lt;/i&gt;", "Hello &lt;i&gt;world&lt;/i&gt;"),
        ("Hello <b>&lt;i&gt;world&lt;/i&gt;</b>", "Hello &lt;i&gt;world&lt;/i&gt;"),
    ),
)
def test_strip_tags(tagged_string, expected):
    assert strip_tags(tagged_string) == expected


@pytest.mark.usefixtures("gb_locale")
@pytest.mark.parametrize(
    "currency, symbol",
    (
        ("GBP", "£"),
        ("EUR", "€"),
        ("USD", "US$"),
        ("JPY", "JP¥"),
        ("", ""),
    ),
)
def test_get_currency_symbol(currency, symbol):
    assert get_currency_symbol(currency) == symbol


def test_get_formatted_currency_with_no_value():
    assert get_formatted_currency("") == ""


@pytest.mark.usefixtures("gb_locale")
@pytest.mark.parametrize(
    "number, formatted_number",
    (
        (123, "123"),
        ("123.4", "123.4"),
        ("123.40", "123.4"),
        ("1000", "1,000"),
        ("10000", "10,000"),
        ("100000000", "100,000,000"),
        (0, "0"),
        (0.00, "0"),
        ("", ""),
        (None, ""),
        (Undefined(), ""),
    ),
)
def test_format_number(number, formatted_number):
    assert format_number(number) == formatted_number


def test_format_date_time_in_bst(mock_autoescape_context, app):
    # Given a date after BST started
    date_time = datetime(2018, 3, 29, 23, 59, 0, tzinfo=timezone.utc)

    # When
    with app.test_request_context("/"):
        format_value = format_datetime(mock_autoescape_context, date_time)

    # Then
    assert format_value == "<span class='date'>30 March 2018 at 00:59</span>"


@pytest.mark.parametrize(
    "date_time, formatted_datetime",
    (
        (
            datetime(2018, 10, 28, 00, 15, 0, tzinfo=timezone.utc),
            "28 October 2018 at 01:15",
        ),
        # Clocks go back on 29th Oct 2018
        (
            datetime(2018, 10, 29, 00, 15, 0, tzinfo=timezone.utc),
            "29 October 2018 at 00:15",
        ),
    ),
)
def test_format_date_time_in_gmt(
    app, mock_autoescape_context, date_time, formatted_datetime
):
    date_time = date_time.replace(tzinfo=timezone.utc)
    with app.test_request_context("/"):
        assert (
            format_datetime(mock_autoescape_context, date_time)
            == f"<span class='date'>{formatted_datetime}</span>"
        )


@pytest.mark.parametrize(
    "percentage, formatted_percentage",
    (
        ("100", "100%"),
        (100, "100%"),
        (4.5, "4.5%"),
    ),
)
def test_format_percentage(percentage, formatted_percentage):
    assert format_percentage(percentage) == formatted_percentage


@pytest.mark.usefixtures("app")
@pytest.mark.parametrize(
    "unit, value, length, formatted_unit, language",
    (
        ("length-meter", 100, "short", "100 m", "en_GB"),
        ("length-centimeter", 100, "short", "100 cm", "en_GB"),
        ("length-mile", 100, "short", "100 mi", "en_GB"),
        ("length-kilometer", 100, "short", "100 km", "en_GB"),
        ("area-square-meter", 100, "short", "100 m²", "en_GB"),
        ("area-square-centimeter", 100, "short", "100 cm²", "en_GB"),
        ("area-square-kilometer", 100, "short", "100 km²", "en_GB"),
        ("area-square-mile", 100, "short", "100 sq mi", "en_GB"),
        ("area-hectare", 100, "short", "100 ha", "en_GB"),
        ("area-acre", 100, "short", "100 ac", "en_GB"),
        ("volume-cubic-meter", 100, "short", "100 m³", "en_GB"),
        ("volume-cubic-centimeter", 100, "short", "100 cm³", "en_GB"),
        ("volume-liter", 100, "short", "100 l", "en_GB"),
        ("volume-hectoliter", 100, "short", "100 hl", "en_GB"),
        ("volume-megaliter", 100, "short", "100 Ml", "en_GB"),
        ("duration-hour", 100, "short", "100 hrs", "en_GB"),
        ("duration-hour", 100, "long", "100 hours", "en_GB"),
        ("duration-year", 100, "long", "100 years", "en_GB"),
        ("duration-hour", 100, "short", "100 awr", "cy"),
        ("duration-year", 100, "short", "100 bl", "cy"),
        ("duration-hour", 100, "long", "100 awr", "cy"),
        ("duration-year", 100, "long", "100 mlynedd", "cy"),
        ("mass-metric-ton", 100, "long", "100 tonnes", "en_GB"),
        ("mass-metric-ton", 1, "long", "1 tonne", "en_GB"),
        ("mass-metric-ton", 100, "short", "100 t", "en_GB"),
    ),
)
def test_format_unit(unit, value, length, formatted_unit, language, mocker):
    mocker.patch(
        "app.jinja_filters.flask_babel.get_locale", mocker.Mock(return_value=language)
    )
    assert format_unit(unit, value, length=length) == formatted_unit


@pytest.mark.usefixtures("app")
@pytest.mark.parametrize(
    "unit, length, formatted_unit, language",
    (
        ("length-meter", "short", "m", "en_GB"),
        ("length-centimeter", "short", "cm", "en_GB"),
        ("length-mile", "short", "mi", "en_GB"),
        ("length-kilometer", "short", "km", "en_GB"),
        ("area-square-meter", "short", "m²", "en_GB"),
        ("area-square-centimeter", "short", "cm²", "en_GB"),
        ("area-square-kilometer", "short", "km²", "en_GB"),
        ("area-square-mile", "short", "sq mi", "en_GB"),
        ("area-hectare", "short", "ha", "en_GB"),
        ("area-acre", "short", "ac", "en_GB"),
        ("volume-cubic-meter", "short", "m³", "en_GB"),
        ("volume-cubic-centimeter", "short", "cm³", "en_GB"),
        ("volume-liter", "short", "l", "en_GB"),
        ("volume-hectoliter", "short", "hl", "en_GB"),
        ("volume-megaliter", "short", "Ml", "en_GB"),
        ("duration-hour", "short", "hr", "en_GB"),
        ("duration-year", "short", "yr", "en_GB"),
        ("length-meter", "long", "metres", "en_GB"),
        ("length-centimeter", "long", "centimetres", "en_GB"),
        ("length-mile", "long", "miles", "en_GB"),
        ("length-kilometer", "long", "kilometres", "en_GB"),
        ("area-square-meter", "long", "square metres", "en_GB"),
        ("area-square-centimeter", "long", "square centimetres", "en_GB"),
        ("area-square-kilometer", "long", "square kilometres", "en_GB"),
        ("area-square-mile", "long", "square miles", "en_GB"),
        ("area-hectare", "long", "hectares", "en_GB"),
        ("area-acre", "long", "acres", "en_GB"),
        ("volume-cubic-meter", "long", "cubic metres", "en_GB"),
        ("volume-cubic-centimeter", "long", "cubic centimetres", "en_GB"),
        ("volume-liter", "long", "litres", "en_GB"),
        ("volume-hectoliter", "long", "hectolitres", "en_GB"),
        ("volume-megaliter", "long", "megalitres", "en_GB"),
        ("duration-hour", "long", "hours", "en_GB"),
        ("duration-year", "long", "years", "en_GB"),
        ("duration-hour", "short", "awr", "cy"),
        ("duration-hour", "long", "awr", "cy"),
        ("duration-year", "short", "bl", "cy"),
        ("duration-year", "long", "flynedd", "cy"),
        ("mass-metric-ton", "long", "tonnes", "en_GB"),
        ("mass-metric-ton", "short", "t", "en_GB"),
    ),
)
def test_format_unit_input_label(unit, length, formatted_unit, language, mocker):
    mocker.patch(
        "app.jinja_filters.flask_babel.get_locale", mocker.Mock(return_value=language)
    )
    assert format_unit_input_label(unit, unit_length=length) == formatted_unit


@pytest.mark.parametrize(
    "duration, formatted_duration",
    (
        ({"years": 5, "months": 4}, "5 years 4 months"),
        ({"years": 5, "months": 0}, "5 years"),
        ({"years": 0, "months": 4}, "4 months"),
        ({"years": 1, "months": 1}, "1 year 1 month"),
        ({"years": 0, "months": 0}, "0 months"),
        ({"years": 5}, "5 years"),
        ({"years": 1}, "1 year"),
        ({"years": 0}, "0 years"),
        ({"months": 5}, "5 months"),
        ({"months": 1}, "1 month"),
        ({"months": 0}, "0 months"),
    ),
)
def test_format_duration(duration, formatted_duration, app):
    with app.test_request_context("/"):
        assert format_duration(duration) == formatted_duration


@pytest.mark.parametrize(
    "answer, width",
    (
        ({}, 15),
        ({"maximum": {"value": 1}}, 1),
        ({"maximum": {"value": 123456}}, 6),
        ({"maximum": {"value": 12345678901}}, 15),
        ({"minimum": {"value": -123456}, "maximum": {"value": 1234}}, 7),
        ({"decimal_places": 2, "maximum": {"value": 123456}}, 8),
        ({"maximum": {"value": 999_999_999_999_999}}, 15),
        ({"decimal_places": 5, "maximum": {"value": 999_999_999_999_999}}, 20),
        ({"decimal_places": 6, "maximum": {"value": 999_999_999_999_999}}, 30),
        ({"minimum": {"value": -99_999_999_999_999}}, 15),
        ({"decimal_places": 5, "minimum": {"value": -99_999_999_999_999}}, 20),
        ({"decimal_places": 6, "minimum": {"value": -99_999_999_999_999}}, 30),
        (
            {"maximum": {"value": 123456789012345678901123456789012345678901234567890}},
            None,
        ),
    ),
)
def test_get_width_for_number(answer, width):
    assert get_width_for_number(answer) == width


@pytest.mark.parametrize(
    "question, expected",
    (
        ({"type": "DateRange"}, False),
        ({"type": "MutuallyExclusive", "answers": []}, True),
        ({"type": "General", "answers": [{"type": "Radio"}]}, True),
        ({"type": "General", "answers": [{"type": "Date"}]}, True),
        ({"type": "General", "answers": [{"type": "MonthYearDate"}]}, True),
        ({"type": "General", "answers": [{"type": "Duration"}]}, True),
        ({"type": "General", "answers": [{"type": "Address"}]}, True),
        ({"type": "General", "answers": [{"type": "Relationship"}]}, True),
        ({"type": "General", "answers": [{"type": "Checkbox"}]}, True),
        ({"type": "General", "answers": [{"type": "Radio", "label": "Label"}]}, False),
        ({"type": "General", "answers": [{"type": "Date", "label": "Label"}]}, False),
        (
            {
                "type": "General",
                "answers": [{"type": "MonthYearDate", "label": "Label"}],
            },
            False,
        ),
        (
            {"type": "General", "answers": [{"type": "Duration", "label": "Label"}]},
            False,
        ),
        (
            {"type": "General", "answers": [{"type": "Address", "label": "Label"}]},
            False,
        ),
        (
            {
                "type": "General",
                "answers": [{"type": "Relationship", "label": "Label"}],
            },
            False,
        ),
        (
            {"type": "General", "answers": [{"type": "Checkbox", "label": "Label"}]},
            False,
        ),
        (
            {
                "type": "General",
                "answers": [{"type": "TextField"}, {"type": "TextField"}],
            },
            True,
        ),
    ),
)
def test_should_wrap_with_fieldset(question, expected):
    assert should_wrap_with_fieldset(question) == expected


def test_map_list_collector_config_no_actions():
    list_items = [
        {"item_title": "Mark Bloggs", "list_item_id": "one"},
        {"item_title": "Joe Bloggs", "list_item_id": "two"},
    ]

    output = map_list_collector_config(list_items, True, False)

    expected = [
        {
            "rowItems": [
                {
                    "actions": [],
                    "iconType": None,
                    "id": "one",
                    "rowTitleAttributes": {
                        "data-list-item-id": "one",
                        "data-qa": "list-item-1-label",
                    },
                    "rowTitle": "Mark Bloggs",
                }
            ]
        },
        {
            "rowItems": [
                {
                    "actions": [],
                    "iconType": None,
                    "id": "two",
                    "rowTitleAttributes": {
                        "data-list-item-id": "two",
                        "data-qa": "list-item-2-label",
                    },
                    "rowTitle": "Joe Bloggs",
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
            "id": "primary",
            "list_item_id": "primary",
        },
        {
            "remove_link": "/nonprimary/remove",
            "edit_link": "/nonprimary/change",
            "primary_person": False,
            "item_title": "Joe Bloggs",
            "id": "nonprimary",
            "list_item_id": "nonprimary",
        },
    ]

    output = map_list_collector_config(
        list_items,
        True,
        False,
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
                    "iconType": None,
                    "id": "primary",
                    "rowTitleAttributes": {
                        "data-list-item-id": "primary",
                        "data-qa": "list-item-1-label",
                    },
                    "rowTitle": "Mark Bloggs (You)",
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
                    "iconType": None,
                    "id": "nonprimary",
                    "rowTitleAttributes": {
                        "data-list-item-id": "nonprimary",
                        "data-qa": "list-item-2-label",
                    },
                    "rowTitle": "Joe Bloggs",
                }
            ]
        },
    ]

    assert output == expected


@pytest.mark.usefixtures("gb_locale")
def test_map_list_collector_config_with_related_answers_and_answer_title():
    list_items = [
        {
            "remove_link": "/nonprimary/remove",
            "edit_link": "/nonprimary/change",
            "primary_person": False,
            "item_title": "Name of UK company or branch",
            "id": "nonprimary",
            "list_item_id": "VHoiow",
        },
    ]

    output = map_list_collector_config(
        list_items,
        True,
        False,
        "edit_link_text",
        "edit_link_aria_label",
        "remove_link_text",
        "remove_link_aria_label",
        {
            "VHoiow": [
                {
                    "id": "edit-company",
                    "title": None,
                    "number": None,
                    "question": {
                        "id": "add-question",
                        "type": "General",
                        "title": " ",
                        "number": None,
                        "answers": [
                            {
                                "id": "registration-number",
                                "label": "Registration number",
                                "value": 123,
                                "type": "number",
                                "unit": None,
                                "unit_length": None,
                                "currency": None,
                                "link": "registration_edit_link_url",
                            },
                            {
                                "id": "authorised-insurer-radio",
                                "label": "Is this UK company or branch an authorised insurer?",
                                "value": {"label": "Yes", "detail_answer_value": None},
                                "type": "radio",
                                "unit": None,
                                "unit_length": None,
                                "currency": None,
                                "link": "authorised_edit_link_url",
                            },
                        ],
                    },
                }
            ]
        },
        "Name of UK company or branch",
        "",
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
                            "url": "/nonprimary/change",
                        },
                        {
                            "ariaLabel": "remove_link_aria_label",
                            "attributes": {"data-qa": "list-item-remove-1-link"},
                            "text": "remove_link_text",
                            "url": "/nonprimary/remove",
                        },
                    ],
                    "iconType": None,
                    "id": "VHoiow",
                    "rowTitle": "Name of UK company or branch",
                    "rowTitleAttributes": {
                        "data-list-item-id": "VHoiow",
                        "data-qa": "list-item-1-label",
                    },
                    "valueList": [{"text": "Name of UK company or branch"}],
                },
                {
                    "actions": [
                        {
                            "ariaLabel": "edit_link_aria_label Registration number",
                            "attributes": {
                                "data-ga": "click",
                                "data-ga-action": "Edit click",
                                "data-ga-category": "Summary",
                                "data-qa": "registration-number-edit",
                            },
                            "text": "edit_link_text",
                            "url": "registration_edit_link_url",
                        }
                    ],
                    "attributes": {"data-qa": "registration-number"},
                    "id": "registration-number",
                    "rowTitle": "Registration number",
                    "rowTitleAttributes": {"data-qa": "registration-number-label"},
                    "valueList": [{"text": "123"}],
                },
                {
                    "actions": [
                        {
                            "ariaLabel": "edit_link_aria_label Is this UK "
                            "company or branch an authorised "
                            "insurer?",
                            "attributes": {
                                "data-ga": "click",
                                "data-ga-action": "Edit click",
                                "data-ga-category": "Summary",
                                "data-qa": "authorised-insurer-radio-edit",
                            },
                            "text": "edit_link_text",
                            "url": "authorised_edit_link_url",
                        }
                    ],
                    "attributes": {"data-qa": "authorised-insurer-radio"},
                    "id": "authorised-insurer-radio",
                    "rowTitle": "Is this UK company or branch an authorised "
                    "insurer?",
                    "rowTitleAttributes": {"data-qa": "authorised-insurer-radio-label"},
                    "valueList": [{"text": "Yes"}],
                },
            ]
        }
    ]

    assert to_dict(output) == to_dict(expected)


@pytest.mark.parametrize(
    "address_fields, formatted_address",
    (
        (
            {
                "line": "7 Evelyn Street",
                "town": "Barry",
                "postcode": "CF63 4JG",
            },
            "7 Evelyn Street<br>Barry<br>CF63 4JG",
        ),
        (
            {
                "line": "7 Evelyn Street",
                "town": "Barry",
                "postcode": "CF63 4JG",
                "uprn": "64037876",
            },
            "7 Evelyn Street<br>Barry<br>CF63 4JG",
        ),
    ),
)
def test_get_formatted_address(address_fields, formatted_address):
    assert get_formatted_address(address_fields) == formatted_address


@pytest.mark.parametrize(
    "max_value, expected_width",
    [
        (None, 15),
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


def test_other_config_dropdown_input_type(answer_schema_dropdown, mocker):
    other = OtherConfig(mocker.MagicMock(), answer_schema_dropdown)
    assert other.otherType == "select"


def test_other_config_dropdown_has_options_attribute(answer_schema_dropdown, mocker):
    other = OtherConfig(mocker.MagicMock(), answer_schema_dropdown)
    assert hasattr(other, "options")
    assert not hasattr(other, "value")


def test_other_config_non_dropdown_has_value_attribute(answer_schema_textfield, mocker):
    other = OtherConfig(mocker.MagicMock(), answer_schema_textfield)
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


@pytest.mark.usefixtures("gb_locale")
def test_calculated_summary_config():
    expected = [
        SummaryRow(
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
                        "link": "/questionnaire/first-number-block/?return_to=final-summary&return_to_answer_id=first-number-answer#first-number-answer",
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
                        "link": "/questionnaire/second-number-block/?return_to=final-summary&return_to_answer_id=second-number-answer#second-number-answer",
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
                                "link": (
                                    "/questionnaire/first-number-block/?return_to=final-summary"
                                    "&return_to_answer_id=first-number-answer#first-number-answer"
                                ),
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
                                "link": (
                                    "/questionnaire/second-number-block/?return_to=final-summary"
                                    "&return_to_answer_id=second-number-answer#second-number-answer"
                                ),
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


@pytest.mark.usefixtures("gb_locale")
def test_summary_item_config_with_list_collector():
    expected = [
        {
            "rowItems": [
                {
                    "actions": [
                        {
                            "ariaLabel": "Change your answer for:",
                            "attributes": {"data-qa": "list-item-change-1-link"},
                            "text": "Change",
                            "url": "change_link_url",
                        },
                        {
                            "ariaLabel": "Remove Company A",
                            "attributes": {"data-qa": "list-item-remove-1-link"},
                            "text": "Remove",
                            "url": "remove_link_url",
                        },
                    ],
                    "iconType": None,
                    "id": "vmmPmD",
                    "rowTitle": "Company A",
                    "rowTitleAttributes": {
                        "data-list-item-id": "vmmPmD",
                        "data-qa": "list-item-1-label",
                    },
                },
                {
                    "actions": [
                        {
                            "ariaLabel": "Change your answer for: "
                            "Registration number",
                            "attributes": {
                                "data-ga": "click",
                                "data-ga-action": "Edit click",
                                "data-ga-category": "Summary",
                                "data-qa": "registration-number-edit",
                            },
                            "text": "Change",
                            "url": "edit_link_url",
                        }
                    ],
                    "attributes": {"data-qa": "registration-number"},
                    "id": "registration-number",
                    "rowTitle": "Registration number",
                    "rowTitleAttributes": {"data-qa": "registration-number-label"},
                    "valueList": [{"text": "123"}],
                },
                {
                    "actions": [
                        {
                            "ariaLabel": "Change your answer for: Is this UK "
                            "company or branch an authorised "
                            "insurer?",
                            "attributes": {
                                "data-ga": "click",
                                "data-ga-action": "Edit click",
                                "data-ga-category": "Summary",
                                "data-qa": "authorised-insurer-radio-edit",
                            },
                            "text": "Change",
                            "url": "edit_link_url",
                        }
                    ],
                    "attributes": {"data-qa": "authorised-insurer-radio"},
                    "id": "authorised-insurer-radio",
                    "rowTitle": "Is this UK company or branch an authorised "
                    "insurer?",
                    "rowTitleAttributes": {"data-qa": "authorised-insurer-radio-label"},
                    "valueList": [{"text": "Yes"}],
                },
            ]
        }
    ]

    result = map_summary_item_config(
        group={
            "blocks": [
                {
                    "title": "Companies or UK branches",
                    "type": "List",
                    "add_link": "/questionnaire/companies/add-company/?return_to=section-summary",
                    "add_link_text": "Add another UK company or branch",
                    "empty_list_text": "No UK company or branch added",
                    "list_name": "companies",
                    "related_answers": {
                        "vmmPmD": [
                            {
                                "id": "edit-company",
                                "title": None,
                                "number": None,
                                "question": {
                                    "id": "add-question",
                                    "type": "General",
                                    "title": " ",
                                    "number": None,
                                    "answers": [
                                        {
                                            "id": "registration-number",
                                            "label": "Registration number",
                                            "value": 123,
                                            "type": "number",
                                            "unit": None,
                                            "unit_length": None,
                                            "currency": None,
                                            "link": "edit_link_url",
                                        },
                                        {
                                            "id": "authorised-insurer-radio",
                                            "label": "Is this UK company or branch an authorised insurer?",
                                            "value": {
                                                "label": "Yes",
                                                "detail_answer_value": None,
                                            },
                                            "type": "radio",
                                            "unit": None,
                                            "unit_length": None,
                                            "currency": None,
                                            "link": "edit_link_url",
                                        },
                                    ],
                                },
                            }
                        ]
                    },
                    "answer_title": "Name of UK company or branch",
                    "list": {
                        "list_items": [
                            {
                                "item_title": "Company A",
                                "primary_person": False,
                                "list_item_id": "vmmPmD",
                                "edit_link": "change_link_url",
                                "remove_link": "remove_link_url",
                            }
                        ],
                        "editable": True,
                    },
                }
            ],
        },
        summary_type="SectionSummary",
        answers_are_editable=True,
        no_answer_provided="No answer Provided",
        remove_link_aria_label="Remove Company A",
        remove_link_text="Remove",
        edit_link_text="Change",
        edit_link_aria_label="Change your answer for:",
        calculated_question={},
    )

    assert to_dict(expected) == to_dict(result)


def to_dict(obj):
    return json.loads(json.dumps(obj, default=lambda o: o.__dict__))
