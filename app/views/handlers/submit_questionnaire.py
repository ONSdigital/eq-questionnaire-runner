from __future__ import annotations

from functools import cached_property
from typing import Optional, Union

from app.data_models import QuestionnaireStore
from app.questionnaire import QuestionnaireSchema
from app.questionnaire.location import InvalidLocationException
from app.questionnaire.router import Router
from app.views.contexts import SubmitQuestionnaireContext
from app.views.handlers.submission import SubmissionHandler


class SubmitQuestionnaireHandler:
    def __init__(
        self,
        schema: QuestionnaireSchema,
        questionnaire_store: QuestionnaireStore,
        language: str,
    ):
        if not schema.is_flow_linear:
            raise InvalidLocationException("Submit page not enabled")

        self._schema = schema
        self._questionnaire_store = questionnaire_store
        self._language = language

    @cached_property
    def router(self) -> Router:
        return Router(
            schema=self._schema,
            answer_store=self._questionnaire_store.answer_store,
            list_store=self._questionnaire_store.list_store,
            progress_store=self._questionnaire_store.progress_store,
            metadata=self._questionnaire_store.metadata,
            response_metadata=self._questionnaire_store.response_metadata,
        )

    def get_context(self) -> dict[str, Union[str, dict]]:
        submit_questionnaire_context = SubmitQuestionnaireContext(
            language=self._language,
            schema=self._schema,
            answer_store=self._questionnaire_store.answer_store,
            list_store=self._questionnaire_store.list_store,
            progress_store=self._questionnaire_store.progress_store,
            metadata=self._questionnaire_store.metadata,
            response_metadata=self._questionnaire_store.response_metadata,
        )
        return submit_questionnaire_context()

    def get_previous_location_url(self) -> Optional[str]:
        return self.router.get_last_location_in_questionnaire_url()

    @property
    def template(self) -> str:
        return "submit-with-summary" if self._schema.get_summary_options() else "submit"

    def handle_post(self) -> None:
        submission_handler = SubmissionHandler(
            self._schema, self._questionnaire_store, self.router.full_routing_path()
        )
        submission_handler.submit_questionnaire()
