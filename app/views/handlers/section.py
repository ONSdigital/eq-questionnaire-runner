from typing import Mapping

from app.data_models import QuestionnaireStore
from app.questionnaire import QuestionnaireSchema
from app.questionnaire.location import InvalidLocationException, Location, SectionKey
from app.questionnaire.router import Router
from app.views.contexts import SectionSummaryContext


class SectionHandler:
    def __init__(
        self,
        schema: QuestionnaireSchema,
        questionnaire_store: QuestionnaireStore,
        section_id: str,
        list_item_id: str | None,
        language: str,
    ):
        self._schema = schema
        self._questionnaire_store = questionnaire_store
        self._section_id = section_id
        self._list_item_id = list_item_id
        self._language = language
        self._router = Router(
            schema=schema,
            answer_store=questionnaire_store.answer_store,
            list_store=questionnaire_store.list_store,
            progress_store=questionnaire_store.progress_store,
            metadata=questionnaire_store.metadata,
            response_metadata=questionnaire_store.response_metadata,
            supplementary_data_store=questionnaire_store.supplementary_data_store,
        )
        if not self._is_valid_location():
            raise InvalidLocationException(f"location {self._section_id} is not valid")

        self.current_location = Location(
            section_id=self._section_id,
            list_name=self._schema.get_repeating_list_for_section(self._section_id),
            list_item_id=self._list_item_id,
        )

        self._routing_path = self._router.routing_path(
            SectionKey(section_id=self._section_id, list_item_id=self._list_item_id)
        )

    def get_context(self) -> Mapping:
        section_summary_context = SectionSummaryContext(
            self._language,
            self._schema,
            self._questionnaire_store.answer_store,
            self._questionnaire_store.list_store,
            self._questionnaire_store.progress_store,
            self._questionnaire_store.metadata,
            self._questionnaire_store.response_metadata,
            self._routing_path,
            self.current_location,
            self._questionnaire_store.supplementary_data_store,
        )
        return section_summary_context()

    def get_next_location_url(self) -> str:
        return self._router.get_next_location_url_for_end_of_section()

    def get_previous_location_url(self) -> str:
        return self._router.get_last_location_in_section(self._routing_path).url()

    def get_resume_url(self) -> str:
        return self._router.get_section_resume_url(self._routing_path)

    def can_display_summary(self) -> bool:
        return self._router.can_display_section_summary(
            SectionKey(self._section_id, self._list_item_id)
        )

    def _is_valid_location(self) -> bool:
        return self._section_id in self._router.enabled_section_ids
