from datetime import datetime, timedelta, timezone
from typing import Mapping, Union

from flask import current_app

from app.data_models import QuestionnaireStore
from app.data_models.session_data import SessionData
from app.questionnaire import QuestionnaireSchema
from app.views.contexts.submitted_response_context import (
    build_submitted_response_context,
)


class SubmittedResponseNotEnabled(Exception):
    pass


class SubmittedResponseExpired(Exception):
    pass


class SubmittedResponse:
    def __init__(
        self,
        schema: QuestionnaireSchema,
        questionnaire_store: QuestionnaireStore,
        session_data: SessionData,
        language: str,
    ):
        self._schema = schema
        self._session_data: SessionData = session_data
        submission_schema: Mapping = self._schema.get_submission() or {}

        if not submission_schema.get("view_response"):
            raise SubmittedResponseNotEnabled

        self._questionnaire_store = questionnaire_store

        expiration_time = self._questionnaire_store.submitted_at + timedelta(
            seconds=current_app.config["SUBMITTED_RESPONSE_EXPIRATION_IN_SECONDS"]
        )

        if datetime.now(timezone.utc) >= expiration_time:
            raise SubmittedResponseExpired

        self._language = language

    def get_context(self) -> dict[str, Union[str, datetime, dict]]:
        context = build_submitted_response_context(
            self._language,
            self._schema,
            self._questionnaire_store,
            self._session_data,
        )
        return context

    def get_page_title(self) -> str:
        return "Submitted Response"
