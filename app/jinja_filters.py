# coding: utf-8

import re
from datetime import datetime
from decimal import Decimal
from typing import Any, Callable, Literal, Mapping, Optional, TypeAlias, Union

import flask
import flask_babel
from babel import numbers
from flask import current_app, g
from jinja2 import nodes, pass_eval_context
from markupsafe import Markup, escape
from wtforms import SelectFieldBase

from app.questionnaire.questionnaire_schema import (
    QuestionnaireSchema,
    is_summary_with_calculation,
)
from app.questionnaire.rules.utils import parse_datetime
from app.settings import MAX_NUMBER
from app.utilities.decimal_places import (
    custom_format_decimal,
    custom_format_unit,
    get_formatted_currency,
)

blueprint = flask.Blueprint("filters", __name__)
FormType = Mapping[str, Mapping[str, Any]]
AnswerType = Mapping[str, Any]
UnitLengthType: TypeAlias = Literal["short", "long", "narrow"]


def mark_safe(context: nodes.EvalContext, value: str) -> Union[Markup, str]:
    return Markup(value) if context.autoescape else value


def strip_tags(value: str) -> Markup:
    return escape(Markup(value).striptags())


@blueprint.app_template_filter()
def format_number(value: int | Decimal | float) -> str:
    locale = flask_babel.get_locale()

    formatted_number: str = custom_format_decimal(value, locale)
    return formatted_number


def get_formatted_address(address_fields: dict[str, str]) -> str:
    address_fields.pop("uprn", None)
    return "<br>".join(address_field for address_field in address_fields.values())


@blueprint.app_template_filter()
def get_currency_symbol(currency: str = "GBP") -> str:
    currency_symbol: str = numbers.get_currency_symbol(
        currency, locale=flask_babel.get_locale()
    )
    return currency_symbol


@blueprint.app_template_filter()
def format_percentage(value: Union[int, float, Decimal]) -> str:
    return f"{value}%"


def format_unit(
    unit: str,
    value: int | float | Decimal,
    length: UnitLengthType = "short",
) -> str:
    formatted_unit: str = custom_format_unit(
        value=value,
        measurement_unit=unit,
        length=length,
        locale=flask_babel.get_locale(),
    )

    return formatted_unit


def format_unit_input_label(unit: str, unit_length: UnitLengthType = "short") -> str:
    """
    This function is used to only get the unit of measurement text. If the unit_length
    is long then only the plural form of the word is returned (e.g., Hours, Years, etc).

    :param (str) unit unit of measurement
    :param (str) unit_length length of unit text, can be one of short/long/narrow
    """
    unit_label: str

    if unit_length == "long":
        unit_label = format_unit(value=2, unit=unit, length=unit_length).replace(
            "2 ", ""
        )
    else:
        # Type ignore: We pass an empty string  as the value so that we just return the unit label
        unit_label = format_unit(
            value="", unit=unit, length=unit_length  # type: ignore
        ).strip()

    return unit_label


def format_duration(value: Mapping[str, int]) -> str:
    parts = []

    if "years" in value and (value["years"] > 0 or len(value) == 1):
        parts.append(
            flask_babel.ngettext("%(num)s year", "%(num)s years", value["years"])
        )
    if "months" in value and (
        value["months"] > 0
        or len(value) == 1
        or ("years" in value and value["years"] == 0)
    ):
        parts.append(
            flask_babel.ngettext("%(num)s month", "%(num)s months", value["months"])
        )
    return " ".join(parts)


def get_format_multilined_string(value: str) -> str:
    escaped_value = escape(value)
    new_line_regex = r"(?:\r\n|\r|\n)+"
    value_with_line_break_tag = re.sub(new_line_regex, "<br>", escaped_value)
    return f"{value_with_line_break_tag}"


def get_format_date(value: Markup) -> str:
    """Format a datetime string.

    :param (jinja2.nodes.EvalContext) context: Evaluation context.
    :param (any) value: Value representing a datetime.
    :returns (str): Formatted datetime.
    """
    value = value[0] if isinstance(value, list) else value
    date_format = "d MMMM yyyy"
    if value and re.match(r"\d{4}-\d{2}$", value):
        date_format = "MMMM yyyy"
    if value and re.match(r"\d{4}$", value):
        date_format = "yyyy"

    date_to_format = parse_datetime(value).date()

    date = flask_babel.format_date(date_to_format, format=date_format)

    return f"<span class='date'>{date}</span>"


@pass_eval_context
@blueprint.app_template_filter()
def format_datetime(
    context: nodes.EvalContext, date_time: datetime
) -> Union[str, Markup]:
    # flask babel on formatting will automatically convert based on the time zone specified in setup.py
    formatted_date = flask_babel.format_date(date_time, format="d MMMM yyyy")
    formatted_time = flask_babel.format_time(date_time, format="HH:mm")

    date = flask_babel.gettext(
        "%(date)s at %(time)s", date=formatted_date, time=formatted_time
    )

    result = f"<span class='date'>{date}</span>"

    return mark_safe(context, result)


def get_format_date_range(start_date: Markup, end_date: Markup) -> Markup:
    date_range: Markup
    date_range = flask_babel.gettext(
        "%(from_date)s to %(to_date)s",
        from_date=get_format_date(start_date),
        to_date=get_format_date(end_date),
    )
    return date_range


@blueprint.app_context_processor
def format_unit_processor() -> dict[
    str,
    Callable[[str, int | float | Decimal, UnitLengthType], str],
]:
    return {"format_unit": format_unit}


@blueprint.app_context_processor
def format_unit_input_label_processor() -> dict[str, Callable]:
    return {"format_unit_input_label": format_unit_input_label}


@blueprint.app_context_processor
def get_currency_symbol_processor() -> dict[str, Callable]:
    return {"get_currency_symbol": get_currency_symbol}


@blueprint.app_template_filter()
def setAttribute(dictionary: dict[str, str], key: str, value: str) -> dict[str, str]:
    dictionary[key] = value
    return dictionary


@blueprint.app_template_filter()
def setAttributes(
    dictionary: dict[str, str], attributes: dict[str, str]
) -> dict[str, str]:
    for key in attributes:
        dictionary[key] = attributes[key]
    return dictionary


@blueprint.app_template_filter()
def should_wrap_with_fieldset(question: dict[str, list]) -> bool:
    # Logic for when to wrap with a fieldset comes from
    # https://service-manual.ons.gov.uk/design-system/components/fieldset
    if question["type"] == "DateRange":
        return False

    answers = question["answers"]
    return (
        question["type"] == "MutuallyExclusive"
        or len(answers) > 1
        or (
            answers[0]["type"]
            in [
                "Radio",
                "Date",
                "MonthYearDate",
                "Duration",
                "Address",
                "Relationship",
                "Checkbox",
            ]
            and "label" not in answers[0]
        )
    )


@blueprint.app_context_processor
def should_wrap_with_fieldset_processor() -> dict[str, Callable]:
    return {"should_wrap_with_fieldset": should_wrap_with_fieldset}


def get_min_max_value_width(
    min_max: Literal["minimum", "maximum"], answer: AnswerType, default_value: int
) -> int:
    """
    This function gets the minimum and maximum value accepted for a question.
    Which then allows us to use that value to set the width of the textbox to suit that min and max.

    If the min or max for the answer is a value source but not an "answers" source, such as a calculated or grand calculated summary,
    use the length of the default value for the min and max width, as the actual min and max width cannot currently be determined
    """
    min_max_value = answer.get(min_max, {})
    if min_max_value and isinstance(answer[min_max]["value"], Mapping):
        if answer[min_max]["value"].get("source") == "answers":
            schema: QuestionnaireSchema = g.get("schema")
            identifier = answer[min_max]["value"]["identifier"]
            return schema.min_and_max_map[identifier][min_max]
        return len(str(default_value))

    # Factor out the decimals as it's accounted for in get_width_for_number
    result = int(min_max_value.get("value", default_value))
    return len(str(result))


@blueprint.app_template_filter()
def get_width_for_number(answer: AnswerType) -> Optional[int]:
    allowable_widths = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 30, 40, 50]

    min_value_width = get_min_max_value_width("minimum", answer, 0)
    max_value_width = get_min_max_value_width("maximum", answer, MAX_NUMBER)

    width = max(min_value_width, max_value_width)

    width += answer.get("decimal_places", 0)

    for allowable_width in allowable_widths:
        if width <= allowable_width:
            return allowable_width


@blueprint.app_context_processor
def get_width_for_number_processor() -> dict[str, Callable]:
    return {"get_width_for_number": get_width_for_number}


class LabelConfig:
    def __init__(self, _for: str, text: str, description: Optional[str] = None) -> None:
        self._for = _for
        self.text = text
        self.description = description


class SelectConfig:
    def __init__(
        self,
        option: SelectFieldBase._Option,
        index: int,
        answer: AnswerType,
        form: Optional[FormType] = None,
    ) -> None:
        self.id = option.id
        self.name = option.name
        self.value = option.data
        self.checked = option.checked

        label_description = None

        try:
            self._answer_option = answer.get("options", [])[index]
        except IndexError:
            self._answer_option = {}

        if self._answer_option:
            if "description" in self._answer_option:
                label_description = self._answer_option["description"]

            if form and option.detail_answer_id:
                detail_answer_field = form["fields"][option.detail_answer_id]
                detail_answer_schema = self._answer_option["detail_answer"]

                self.other = OtherConfig(detail_answer_field, detail_answer_schema)

        self.label = LabelConfig(option.id, option.label.text, label_description)


class RelationshipRadioConfig(SelectConfig):
    def __init__(
        self,
        option: SelectFieldBase._Option,
        index: int,
        answer: AnswerType,
    ) -> None:
        super().__init__(option, index, answer)

        if self._answer_option:
            # the 'pre-' prefix is added to the attributes here so that html minification
            # doesn't mess with the attribute contents (the 'pre-' is removed during minification).
            # see https://htmlmin.readthedocs.io/en/latest/quickstart.html
            attribute_key = (
                "pre-" if current_app.config["EQ_ENABLE_HTML_MINIFY"] else ""
            )

            self.attributes = {
                f"{attribute_key}data-title": escape(self._answer_option["title"]),
                f"{attribute_key}data-playback": escape(
                    self._answer_option["playback"]
                ),
            }


class OtherConfig:
    def __init__(
        self,
        detail_answer_field: SelectFieldBase._Option,
        detail_answer_schema: Mapping[str, str],
    ) -> None:
        self.id = detail_answer_field.id
        self.name = detail_answer_field.name

        self.label = LabelConfig(detail_answer_field.id, detail_answer_field.label.text)
        self.open = detail_answer_schema.get("visible", False)
        answer_type = detail_answer_schema["type"]

        if answer_type == "Dropdown":
            self.otherType = "select"
            self.options = [
                DropdownConfig(choice, detail_answer_field)
                for choice in detail_answer_field.choices
            ]
        else:
            self.otherType = "input"
            self.value = escape(detail_answer_field._value())

            if answer_type == "Number":
                self.width = get_width_for_number(detail_answer_schema)


@blueprint.app_template_filter()
def map_select_config(form: FormType, answer: AnswerType) -> list[SelectConfig]:
    options = form["fields"][answer["id"]]

    return [
        SelectConfig(option, index, answer, form)
        for index, option in enumerate(options)
    ]


@blueprint.app_context_processor
def map_select_config_processor() -> dict[str, Callable]:
    return {"map_select_config": map_select_config}


@blueprint.app_template_filter()
def map_relationships_config(
    form: Mapping[str, str], answer: Mapping[str, Union[int, slice]]
) -> list[RelationshipRadioConfig]:
    options = form["fields"][answer["id"]]

    return [
        RelationshipRadioConfig(option, i, answer) for i, option in enumerate(options)
    ]


@blueprint.app_context_processor
def map_relationships_config_processor() -> dict[str, Callable]:
    return {"map_relationships_config": map_relationships_config}


class DropdownConfig:
    def __init__(
        self, option: SelectFieldBase._Option, select: SelectFieldBase._Option
    ) -> None:
        self.value, self.text = option.value, option.label
        self.selected = select.data == self.value
        self.disabled = self.value == "" and select.flags.required


@blueprint.app_template_filter()
def map_dropdown_config(select: SelectFieldBase._Option) -> list[DropdownConfig]:
    return [DropdownConfig(choice, select) for choice in select.choices]


@blueprint.app_context_processor
def map_dropdown_config_processor() -> dict[str, Callable]:
    return {"map_dropdown_config": map_dropdown_config}


class SummaryAction:
    def __init__(
        self,
        answer: SelectFieldBase._Option,
        item_title: str,
        edit_link_text: str,
        edit_link_aria_label: str,
    ) -> None:
        self.text = edit_link_text
        self.visuallyHiddenText = edit_link_aria_label + " " + item_title
        self.url = answer["link"]

        self.attributes = {
            "data-qa": answer["id"] + "-edit",
            "data-ga": "click",
            "data-ga-category": "Summary",
            "data-ga-action": "Edit click",
        }


class SummaryRowItemValue:
    def __init__(self, text: str, other: Optional[str] = None) -> None:
        self.text = text

        if other or other == 0:
            self.other = other


class SummaryRowItem:
    def __init__(  # noqa: C901, R0912 pylint: disable=too-complex, too-many-branches
        self,
        question: SelectFieldBase._Option,
        answer: SelectFieldBase._Option,
        answers_are_editable: bool,
        no_answer_provided: str,
        edit_link_text: str,
        edit_link_aria_label: str,
        summary_type: str,
        use_answer_label: bool = False,
    ) -> None:
        answer_type = answer.get("type", "calculated")
        if (
            answer_type == "relationship"
            or is_summary_with_calculation(summary_type)
            or use_answer_label
        ) and answer.get("label"):
            self.rowTitle = answer["label"]
            self.rowTitleAttributes = {"data-qa": answer["id"] + "-label"}
        else:
            self.rowTitle = strip_tags(question["title"])
            self.rowTitleAttributes = {"data-qa": question["id"]}

        if edit_link_text:
            self.id = answer["id"]

        value = answer["value"]

        self.attributes = {"data-qa": answer["id"]}

        if value is None or value == "":
            self.valueList = [SummaryRowItemValue(no_answer_provided)]
        elif answer_type == "address":
            self.valueList = [SummaryRowItemValue(get_formatted_address(value))]
        elif answer_type == "checkbox":
            self.valueList = [
                SummaryRowItemValue(option["label"], option["detail_answer_value"])
                for option in value
            ]
        elif answer_type == "currency":
            decimal_places = answer.get("decimal_places")
            self.valueList = [
                SummaryRowItemValue(
                    get_formatted_currency(
                        value=value,
                        currency=answer["currency"],
                        decimal_limit=decimal_places,
                    )
                )
            ]
        elif answer_type in ["date", "monthyeardate", "yeardate"]:
            if question["type"] == "DateRange":
                self.valueList = [
                    SummaryRowItemValue(
                        get_format_date_range(value["from"], value["to"])
                    )
                ]
            else:
                self.valueList = [SummaryRowItemValue(get_format_date(value))]
        elif answer_type == "duration":
            self.valueList = [SummaryRowItemValue(format_duration(value))]
        elif answer_type == "number":
            self.valueList = [SummaryRowItemValue(format_number(value))]
        elif answer_type == "percentage":
            self.valueList = [SummaryRowItemValue(format_percentage(value))]
        elif answer_type == "radio":
            detail_answer_value = value["detail_answer_value"]
            self.valueList = [SummaryRowItemValue(value["label"], detail_answer_value)]
        elif answer_type == "textarea":
            self.valueList = [SummaryRowItemValue(get_format_multilined_string(value))]
        elif answer_type == "unit":
            self.valueList = [
                SummaryRowItemValue(
                    format_unit(answer["unit"], value, answer["unit_length"])
                )
            ]
        else:
            self.valueList = [SummaryRowItemValue(value)]

        if answers_are_editable:
            self.actions = [
                SummaryAction(
                    answer, self.rowTitle, edit_link_text, edit_link_aria_label
                )
            ]


class SummaryRow:
    def __init__(
        self,
        question: SelectFieldBase._Option,
        summary_type: SelectFieldBase._Option,
        answers_are_editable: bool,
        no_answer_provided: str,
        edit_link_text: str,
        edit_link_aria_label: str,
        use_answer_label: bool = False,
    ) -> None:
        self.rowTitle = strip_tags(question["title"])
        self.id = question["id"]
        self.rowItems = []
        use_answer_label = use_answer_label or len(question["answers"]) > 1

        if is_summary_with_calculation(summary_type) and not answers_are_editable:
            self.total = True

        for answer in question["answers"]:
            self.rowItems.append(
                SummaryRowItem(
                    question,
                    answer,
                    answers_are_editable,
                    no_answer_provided,
                    edit_link_text,
                    edit_link_aria_label,
                    summary_type,
                    use_answer_label,
                )
            )


@blueprint.app_template_filter()
def map_summary_item_config(
    group: dict[str, Union[list, dict]],
    summary_type: str,
    answers_are_editable: bool,
    no_answer_provided: str,
    edit_link_text: str,
    edit_link_aria_label: str,
    calculated_question: Optional[dict[str, list]],
    remove_link_text: str | None = None,
    remove_link_aria_label: str | None = None,
) -> list[Union[dict[str, list], SummaryRow]]:
    rows: list[Union[dict[str, list], SummaryRow]] = []

    for block in group["blocks"]:
        if block.get("question"):
            rows.append(
                SummaryRow(
                    block["question"],
                    summary_type,
                    answers_are_editable,
                    no_answer_provided,
                    edit_link_text,
                    edit_link_aria_label,
                )
            )
        elif block.get("calculated_summary"):
            rows.append(
                SummaryRow(
                    block["calculated_summary"],
                    summary_type,
                    answers_are_editable,
                    no_answer_provided,
                    edit_link_text,
                    edit_link_aria_label,
                )
            )
        else:
            list_collector_rows = map_list_collector_config(
                list_items=block["list"]["list_items"],
                editable=block["list"]["editable"],
                edit_link_text=edit_link_text,
                edit_link_aria_label=edit_link_aria_label,
                remove_link_text=remove_link_text,
                remove_link_aria_label=remove_link_aria_label,
                related_answers=block.get("related_answers"),
                item_label=block.get("item_label"),
                item_anchor=block.get("item_anchor"),
            )

            rows.extend(list_collector_rows)

    if is_summary_with_calculation(summary_type):
        rows.append(SummaryRow(calculated_question, summary_type, False, "", "", ""))

    return rows


@blueprint.app_context_processor
def map_summary_item_config_processor() -> dict[str, Callable]:
    return {"map_summary_item_config": map_summary_item_config}


# pylint: disable=too-many-locals
@blueprint.app_template_filter()
def map_list_collector_config(
    list_items: list[dict[str, str | int]],
    editable: bool = True,
    render_icon: bool = False,
    edit_link_text: str = "",
    edit_link_aria_label: str = "",
    remove_link_text: str | None = None,
    remove_link_aria_label: str | None = None,
    related_answers: dict | None = None,
    item_label: str | None = None,
    item_anchor: str | None = None,
) -> list[dict[str, list] | SummaryRow]:
    rows: list[dict[str, list] | SummaryRow] = []

    for index, list_item in enumerate(list_items, start=1):
        item_name = list_item.get("item_title")

        actions = []
        edit_link_hidden_text = None
        remove_link_hidden_text = None

        if edit_link_text and editable:
            url = (
                f'{list_item.get("edit_link")}{item_anchor}'
                if item_anchor
                else list_item.get("edit_link")
            )

            edit_link = {
                "text": edit_link_text,
                "visuallyHiddenText": edit_link_hidden_text,
                "url": url,
                "attributes": {"data-qa": f"list-item-change-{index}-link"},
            }

            if edit_link_aria_label:
                edit_link_hidden_text = edit_link_aria_label.format(item_name=item_name)
            edit_link["visuallyHiddenText"] = edit_link_hidden_text

            actions.append(edit_link)

        if not list_item.get("primary_person") and remove_link_text and editable:
            if remove_link_aria_label:
                remove_link_hidden_text = remove_link_aria_label.format(
                    item_name=item_name
                )

            actions.append(
                {
                    "text": remove_link_text,
                    "visuallyHiddenText": remove_link_hidden_text,
                    "url": list_item.get("remove_link"),
                    "attributes": {"data-qa": f"list-item-remove-{index}-link"},
                }
            )

        icon = (
            "check"
            if render_icon
            and list_item.get("repeating_blocks")
            and list_item.get("is_complete")
            else None
        )

        row_item = {
            "iconType": icon,
            "actions": actions,
            "id": list_item.get("list_item_id"),
            "rowTitleAttributes": {
                "data-qa": f"list-item-{index}-label",
                "data-list-item-id": list_item.get("list_item_id"),
            },
        }

        if item_label:
            row_item["valueList"] = [{"text": item_name}]

        row_item["rowTitle"] = item_label or item_name
        row_items: list = [row_item]

        if related_answers:
            for block in related_answers[list_item["list_item_id"]]:
                summary_row = SummaryRow(
                    block["question"],
                    summary_type="SectionSummary",
                    answers_are_editable=True,
                    no_answer_provided=flask_babel.lazy_gettext("No answer provided"),
                    edit_link_text=edit_link_text,
                    edit_link_aria_label=edit_link_aria_label,
                    use_answer_label=True,
                )
                row_items.extend(summary_row.rowItems)

        rows.append({"rowItems": row_items})

    return rows


@blueprint.app_context_processor
def map_list_collector_config_processor() -> dict[str, Callable]:
    return {"map_list_collector_config": map_list_collector_config}
