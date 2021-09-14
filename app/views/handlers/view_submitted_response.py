from datetime import datetime
from typing import Mapping, Union

from flask_babel import lazy_gettext

from app.data_models import QuestionnaireStore
from app.helpers.template_helpers import get_survey_type
from app.questionnaire import QuestionnaireSchema
from app.views.contexts.view_submitted_response_context import (
    build_view_submitted_response_context,
)


class ViewSubmittedResponseNotEnabled(Exception):
    pass


class ViewSubmittedResponse:
    def __init__(
        self,
        schema: QuestionnaireSchema,
        questionnaire_store: QuestionnaireStore,
        language: str,
    ):
        self._schema = schema
        self._questionnaire_store = questionnaire_store
        self._language = language

        submission_schema: Mapping = self._schema.get_post_submission()

        if not submission_schema.get("view_response"):
            raise ViewSubmittedResponseNotEnabled

    def get_context(self) -> dict[str, Union[str, datetime, dict]]:
        return build_view_submitted_response_context(
            self._language, self._schema, self._questionnaire_store, get_survey_type()
        )

    @staticmethod
    def get_page_title() -> str:
        return lazy_gettext("View Submitted Response")
