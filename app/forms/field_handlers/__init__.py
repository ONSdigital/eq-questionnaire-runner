from .address_handler import AddressHandler
from .date_handlers import DateHandler, MonthYearDateHandler, YearDateHandler
from .dropdown_handler import DropdownHandler
from .duration_handler import DurationHandler
from .mobile_number_handler import MobileNumberHandler
from .number_handler import NumberHandler
from .select_handlers import SelectHandler, SelectMultipleHandler
from .string_handler import StringHandler
from .text_area_handler import TextAreaHandler

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
    answer,
    error_messages,
    answer_store,
    metadata=None,
    location=None,
    disable_validation=False,
    question_title=None,
):
    return FIELD_HANDLER_MAPPINGS[answer.get("type")](
        answer,
        error_messages=error_messages,
        answer_store=answer_store,
        metadata=metadata,
        location=location,
        disable_validation=disable_validation,
        question_title=question_title,
    )
