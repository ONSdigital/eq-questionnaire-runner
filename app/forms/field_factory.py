from app.forms.field_handlers.date_handler import DateHandler
from app.forms.field_handlers.dropdown_handler import DropdownHandler
from app.forms.field_handlers.duration_handler import DurationHandler
from app.forms.field_handlers.year_month_date_handler import YearMonthDateHandler
from app.forms.field_handlers.number_handler import NumberHandler
from app.forms.field_handlers.select_handler import SelectHandler
from app.forms.field_handlers.select_multiple_handler import SelectMultipleHandler
from app.forms.field_handlers.string_handler import StringHandler
from app.forms.field_handlers.text_area_handler import TextAreaHandler
from app.forms.field_handlers.year_date_handler import YearDateHandler

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
    'MonthYearDate': YearMonthDateHandler,
    'YearDate': YearDateHandler,
    'Duration': DurationHandler,
}


def get_field(
    answer,
    error_messages,
    answer_store,
    metadata=None,
    location=None,
    disable_validation=False,
):
    return FIELD_HANDLER_MAPPINGS[answer.get('type')](
        answer,
        error_messages=error_messages,
        answer_store=answer_store,
        metadata=metadata,
        location=location,
        disable_validation=disable_validation,
    ).get_field()
