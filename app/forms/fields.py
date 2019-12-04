from app.forms.handlers.date_handler import DateHandler
from app.forms.handlers.dropdown_handler import DropdownHandler
from app.forms.handlers.duration_handler import DurationHandler
from app.forms.handlers.number_handler import NumberHandler
from app.forms.handlers.select_handler import SelectHandler
from app.forms.handlers.select_multiple_handler import SelectMultipleHandler
from app.forms.handlers.string_handler import StringHandler
from app.forms.handlers.text_area_handler import TextAreaHandler

FIELD_HANDLER_MAPPINGS = {
    'Checkbox': SelectMultipleHandler,
    'Radio': SelectHandler,
    'Relationship': SelectHandler,
    'TextArea': TextAreaHandler,
    'TextField': StringHandler,
    'Dropdown': DropdownHandler,
    'Number': NumberHandler,
    'Currency': NumberHandler,
    'Unit': NumberHandler,
    'Percentage': NumberHandler,
    'Date': DateHandler,
    'MonthYearDate': DateHandler,
    'YearDate': DateHandler,
    'Duration': DurationHandler,
}


def get_field(answer, error_messages, answer_store, metadata, disable_validation=False):

    return FIELD_HANDLER_MAPPINGS[answer.get('type')](
        answer,
        error_messages,
        answer_store,
        metadata,
        disable_validation=disable_validation,
    ).get_field()
