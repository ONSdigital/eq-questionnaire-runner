from typing import Optional

from werkzeug.datastructures import ImmutableDict

from app.forms.field_handlers.address_handler import AddressHandler
from app.forms.field_handlers.date_handlers import (
    DateHandler,
    MonthYearDateHandler,
    YearDateHandler,
)
from app.forms.field_handlers.dropdown_handler import DropdownHandler
from app.forms.field_handlers.duration_handler import DurationHandler
from app.forms.field_handlers.field_handler import FieldHandler
from app.forms.field_handlers.mobile_number_handler import MobileNumberHandler
from app.forms.field_handlers.number_handler import NumberHandler
from app.forms.field_handlers.select_handlers import (
    SelectHandler,
    SelectMultipleHandler,
)
from app.forms.field_handlers.string_handler import StringHandler
from app.forms.field_handlers.text_area_handler import TextAreaHandler
from app.questionnaire.rules.rule_evaluator import RuleEvaluator

FIELD_HANDLER_MAPPINGS = {
    "Checkbox": SelectMultipleHandler,
    "Radio": SelectHandler,
    "Relationship": SelectHandler,
    "TextArea": TextAreaHandler,
    "TextField": StringHandler,
    "Dropdown": DropdownHandler,
    "Number": NumberHandler,
    "Currency": NumberHandler,
    "Unit": NumberHandler,
    "Percentage": NumberHandler,
    "Date": DateHandler,
    "MonthYearDate": MonthYearDateHandler,
    "YearDate": YearDateHandler,
    "Duration": DurationHandler,
    "Address": AddressHandler,
    "MobileNumber": MobileNumberHandler,
}


def get_field_handler(
    *,
    answer_schema: dict,
    rule_evaluator: RuleEvaluator,
    error_messages: ImmutableDict,
    disable_validation: bool = False,
    question_title: Optional[str] = None,
) -> FieldHandler:
    return FIELD_HANDLER_MAPPINGS[answer_schema["type"]](
        answer_schema=answer_schema,
        rule_evaluator=rule_evaluator,
        error_messages=error_messages,
        disable_validation=disable_validation,
        question_title=question_title,
    )
