from __future__ import annotations

from typing import Callable, Mapping

from wtforms import Form

from app.forms.fields import IntegerFieldWithSeparator

ErrorMessageType = dict[str, str]


# pylint: disable=no-member
class DurationForm(Form):
    def validate(
        self, extra_validators: dict[str, list[Callable]] | None = None
    ) -> bool:
        super().validate(extra_validators)

        if all(not field.raw_data[0] for field in self._fields.values()):
            if self.mandatory:
                self._set_error("MANDATORY_DURATION")
                return False

            return True

        if "years" in self.units and (self.years.data is None or self.years.data < 0):
            self._set_error("INVALID_DURATION")
            return False

        if "months" in self.units and (
            self.months.data is None or self.months.data < 0
        ):
            self._set_error("INVALID_DURATION")
            return False

        if "years" in self.units and "months" in self.units and self.months.data > 11:
            self._set_error("INVALID_DURATION")
            return False

        return True

    def _set_error(self, key: str) -> None:
        list(self._fields.values())[0].errors = [self.answer_errors[key]]

    @property
    def data(self) -> dict[str, str | None] | None:
        data: dict[str, str | None] = super().data
        if all(value is None for value in data.values()):
            return None
        return data


def get_duration_form(
    answer: Mapping, error_messages: ErrorMessageType
) -> type[DurationForm]:
    class CustomDurationForm(DurationForm):
        mandatory = answer["mandatory"]
        units = answer["units"]
        answer_errors = _get_answer_errors(answer, error_messages)

    if "years" in answer["units"]:
        CustomDurationForm.years = IntegerFieldWithSeparator()

    if "months" in answer["units"]:
        CustomDurationForm.months = IntegerFieldWithSeparator()

    return CustomDurationForm


def _get_answer_errors(
    answer: Mapping, error_messages: ErrorMessageType
) -> dict[str, str]:
    answer_errors = error_messages.copy()

    if "validation" in answer and "messages" in answer["validation"]:
        for error_key, error_message in answer["validation"]["messages"].items():
            answer_errors[error_key] = error_message

    return answer_errors
