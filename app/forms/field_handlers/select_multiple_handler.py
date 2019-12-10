from app.forms.fields.custom_select_multiple_field import CustomSelectMultipleField
from app.forms.field_handlers.select_handler import SelectHandler


class SelectMultipleHandler(SelectHandler):
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
