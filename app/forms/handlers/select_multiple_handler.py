from app.forms.custom_fields import CustomSelectMultipleField
from app.forms.handlers.string_handler import StringHandler


class SelectMultipleHandler(StringHandler):
    MANDATORY_MESSAGE = 'MANDATORY_CHECKBOX'

    def get_field(self):
        return CustomSelectMultipleField(
            label=self.label,
            description=self.guidance,
            choices=self.build_choices_with_detail_answer_ids(self.answer['options']),
            validators=self.validators,
        )
