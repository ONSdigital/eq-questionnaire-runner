from app.forms.custom_fields import CustomSelectMultipleField
from app.forms.handlers.field_handler import FieldHandler


class SelectMultipleHandler(FieldHandler):
    MANDATORY_MESSAGE = 'MANDATORY_CHECKBOX'

    def get_field(self) -> CustomSelectMultipleField:
        return CustomSelectMultipleField(
            label=self.label,
            description=self.guidance,
            choices=self.build_choices_with_detail_answer_ids(
                self.answer_schema['options']
            ),
            validators=self.validators,
        )
