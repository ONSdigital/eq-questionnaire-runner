from __future__ import annotations

from functools import cached_property
from typing import Union

from app.data_models import QuestionnaireStore
from app.questionnaire import QuestionnaireSchema
from app.questionnaire.location import InvalidLocationException
from app.questionnaire.router import Router
from app.views.contexts import SubmitContext
from app.views.handlers.submission import SubmissionHandler


class SubmitHandler:
    def __init__(
        self,
        schema: QuestionnaireSchema,
        questionnaire_store: QuestionnaireStore,
        language: str,
    ):
        self._schema = schema
        self._questionnaire_store = questionnaire_store
        self._language = language

        if not self._schema.is_questionnaire_flow_linear:
            raise InvalidLocationException(
                "Submit page not enabled or questionnaire is not complete"
            )

    @cached_property
    def router(self) -> Router:
        return Router(
            schema=self._schema,
            answer_store=self._questionnaire_store.answer_store,
            list_store=self._questionnaire_store.list_store,
            progress_store=self._questionnaire_store.progress_store,
            metadata=self._questionnaire_store.metadata,
        )

    def get_context(self) -> dict[str, Union[str, dict]]:
        submit_context = SubmitContext(
            language=self._language,
            schema=self._schema,
            answer_store=self._questionnaire_store.answer_store,
            list_store=self._questionnaire_store.list_store,
            progress_store=self._questionnaire_store.progress_store,
            metadata=self._questionnaire_store.metadata,
        )
        return submit_context()

    def get_previous_location_url(self) -> str:
        return self.router.get_last_location_in_questionnaire().url()

    @property
    def template(self) -> str:
        include_summary = self._schema.questionnaire_flow_options["include_summary"]
        return "summary" if include_summary else "confirmation"

    def handle_post(self) -> None:
        submission_handler = SubmissionHandler(
            self._schema, self._questionnaire_store, self.router.full_routing_path()
        )
        submission_handler.submit_questionnaire()
