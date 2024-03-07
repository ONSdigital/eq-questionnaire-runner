"""
Operations.py can't be used in placeholder_transformer due to the circular reference issue
The methods here invoke operations methods, so it can be imported in placeholder transformer
this is a temporary solution until placeholder transformer is refactored.
"""

from datetime import date
from typing import TYPE_CHECKING, Optional

from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.questionnaire.rules.operations import DateOffset, Operations

if TYPE_CHECKING:
    from app.questionnaire.placeholder_renderer import (
        PlaceholderRenderer,  # pragma: no cover
    )


class OperationHelper:
    def __init__(
        self,
        language: str,
        schema: QuestionnaireSchema,
        renderer: "PlaceholderRenderer",
    ):
        self.language = language
        self.schema = schema
        self.renderer = renderer
        self.ops = Operations(language=language, schema=self.schema, renderer=renderer)

    def string_to_datetime(
        self,
        date_string: Optional[str],
        offset: Optional[DateOffset] = None,
        offset_by_full_weeks: bool = False,
    ) -> Optional[date]:
        return self.ops.resolve_date_from_string(
            date_string, offset, offset_by_full_weeks
        )

    def get_option_label_from_value(
        self,
        value: str,
        answer_id: str,
    ) -> str:
        return self.ops.evaluate_option_label_from_value(value, answer_id)
