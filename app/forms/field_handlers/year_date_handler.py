from app.forms.field_handlers.date_handler import DateHandler
from app.forms.fields.year_date_field import YearDateField
from app.forms.validators import SingleDatePeriodCheck


class YearDateHandler(DateHandler):
    DATE_FORMAT = "yyyy"
    DISPLAY_FORMAT = "yyyy"

    def get_field(self) -> YearDateField:
        return YearDateField(
            self.validators, label=self.label, description=self.guidance
        )

    def get_min_max_validator(self, minimum_date, maximum_date):
        messages = self.answer_schema.get("validation", {}).get("messages")

        minimum_date = (
            minimum_date.replace(month=1, day=1) if minimum_date else None
        )  # January 1st
        maximum_date = (
            maximum_date.replace(month=12, day=31) if maximum_date else None
        )  # Last day of december

        return SingleDatePeriodCheck(
            messages=messages,
            date_format=self.DISPLAY_FORMAT,
            minimum_date=minimum_date,
            maximum_date=maximum_date,
        )
