from datetime import datetime

from flask_babel import lazy_gettext

from app.data_models import QuestionnaireStore
from app.globals import has_view_submitted_response_expired
from app.helpers.template_helpers import get_survey_type, render_template
from app.questionnaire import QuestionnaireSchema
from app.views.contexts.view_submitted_response_context import (
    build_view_submitted_response_context,
)


class ViewSubmittedResponseNotEnabled(Exception):
    pass


class ViewSubmittedResponseExpired(Exception):
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

        if not self._schema.is_view_submitted_response_enabled:
            raise ViewSubmittedResponseNotEnabled

    @property
    def has_expired(self) -> bool:
        if self._questionnaire_store.submitted_at:
            return has_view_submitted_response_expired(
                self._questionnaire_store.submitted_at
            )
        return False

    def get_context(self) -> dict[str, str | datetime | dict]:
        return build_view_submitted_response_context(
            self._language, self._schema, self._questionnaire_store, get_survey_type()
        )

    @staticmethod
    def get_page_title() -> str:
        title: str = lazy_gettext("View Submitted Response")
        return title

    def get_rendered_html(self) -> str:
        return render_template(
            template="view-submitted-response",
            content=self.get_context(),
            page_title=self.get_page_title(),
        )
