from app.forms.fields.select_field_with_detail_answer import SelectFieldWithDetailAnswer
from app.forms.field_handlers.field_handler import FieldHandler


class SelectHandler(FieldHandler):
    MANDATORY_MESSAGE_KEY = "MANDATORY_RADIO"

    @staticmethod
    def coerce_str_unless_none(value):
        """
        Coerces a value using str() unless that value is None
        :param value: Any value that can be coerced using str() or None
        :return: str(value) or None if value is None
        """
        return str(value) if value is not None else None

    @staticmethod
    def build_choices_with_detail_answer_ids(options: dict):
        choices = []
        for option in options:
            detail_answer_id = (
                option["detail_answer"]["id"] if option.get("detail_answer") else None
            )
            choices.append((option["value"], option["label"], detail_answer_id))
        return choices

    # We use a custom coerce function to avoid a defect where Python NoneType
    # is coerced to the string 'None' which clashes with legitimate Radio field
    # values of 'None'; i.e. there is no way to differentiate between the user
    # not providing an answer and them selecting the 'None' option otherwise.
    # https://github.com/ONSdigital/eq-survey-runner/issues/1013
    # See related WTForms PR: https://github.com/wtforms/wtforms/pull/288
    def get_field(self) -> SelectFieldWithDetailAnswer:
        return SelectFieldWithDetailAnswer(
            label=self.label,
            description=self.guidance,
            choices=self.build_choices_with_detail_answer_ids(
                self.answer_schema["options"]
            ),
            validators=self.validators,
            coerce=self.coerce_str_unless_none,
        )
