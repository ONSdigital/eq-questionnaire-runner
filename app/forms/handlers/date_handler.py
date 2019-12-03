from app.forms.date_form import DateFormType, DateField, get_date_limits
from app.forms.handlers.field_handler import FieldHandler


class DateHandler(FieldHandler):
    MANDATORY_MESSAGE = 'MANDATORY_RADIO'
    DATE_FIELD_MAP = {
        'Date': DateFormType.YearMonthDay,
        'MonthYearDate': DateFormType.YearMonth,
        'YearDate': DateFormType.Year,
    }

    def get_field(self):
        minimum_date, maximum_date = get_date_limits(
            self.answer, self.answer_store, self.metadata
        )

        return DateField(
            self.DATE_FIELD_MAP[self.answer_type],
            minimum_date,
            maximum_date,
            self.answer,
            self.error_messages,
            label=self.label,
            description=self.guidance,
        )
