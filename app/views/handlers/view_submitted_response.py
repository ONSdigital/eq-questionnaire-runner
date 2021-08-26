from datetime import datetime, timedelta, timezone
from typing import Mapping, Union

from flask import current_app
from flask_babel import lazy_gettext

from app.data_models import QuestionnaireStore
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

        submission_schema: Mapping = self._schema.get_post_submission()

        if not submission_schema.get("view_response"):
            raise ViewSubmittedResponseNotEnabled

        expiration_time = self._questionnaire_store.submitted_at + timedelta(
            seconds=current_app.config["VIEW_SUBMITTED_RESPONSE_EXPIRATION_IN_SECONDS"]
        )

        if datetime.now(timezone.utc) >= expiration_time:
            raise ViewSubmittedResponseExpired

    def get_context(self) -> dict[str, Union[str, datetime, dict]]:
        context = build_view_submitted_response_context(
            self._language, self._schema, self._questionnaire_store
        )
        return context

    @staticmethod
    def get_page_title() -> str:
        return lazy_gettext("View Submitted Response")
