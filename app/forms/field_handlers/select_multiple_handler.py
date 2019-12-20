from app.forms.fields.multiple_select_field_with_detail_answer import (
    MultipleSelectFieldWithDetailAnswer,
)
from app.forms.field_handlers.select_handler import SelectHandler


class SelectMultipleHandler(SelectHandler):
    MANDATORY_MESSAGE_KEY = 'MANDATORY_CHECKBOX'

    def get_field(self) -> MultipleSelectFieldWithDetailAnswer:
        return MultipleSelectFieldWithDetailAnswer(
            label=self.label,
            description=self.guidance,
            choices=self.build_choices_with_detail_answer_ids(
                self.answer_schema['options']
            ),
            validators=self.validators,
        )
