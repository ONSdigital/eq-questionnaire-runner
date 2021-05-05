from app.questionnaire.location import InvalidLocationException, Location
from app.questionnaire.router import Router
from app.views.contexts import SectionSummaryContext


class SectionHandler:
    def __init__(self, schema, questionnaire_store, section_id, list_item_id, language):
        self._schema = schema
        self._questionnaire_store = questionnaire_store
        self._section_id = section_id
        self._list_item_id = list_item_id
        self._language = language
        self._router = Router(
            schema,
            questionnaire_store.answer_store,
            questionnaire_store.list_store,
            questionnaire_store.progress_store,
            questionnaire_store.metadata,
        )
        if not self._is_valid_location():
            raise InvalidLocationException(f"location {self._section_id} is not valid")

        self.current_location = Location(
            section_id=self._section_id,
            list_name=self._schema.get_repeating_list_for_section(self._section_id),
            list_item_id=self._list_item_id,
        )

        self._routing_path = self._router.routing_path(
            section_id=self._section_id, list_item_id=self._list_item_id
        )

    def get_context(self):
        section_summary_context = SectionSummaryContext(
            self._language,
            self._schema,
            self._questionnaire_store.answer_store,
            self._questionnaire_store.list_store,
            self._questionnaire_store.progress_store,
            self._questionnaire_store.metadata,
            self._routing_path,
            self.current_location,
        )
        return section_summary_context()

    def get_next_location_url(self):
        return self._router.get_next_location_url_for_questionnaire_flow()

    def get_previous_location_url(self):
        return self._router.get_last_location_in_section(self._routing_path).url()

    def get_resume_url(self):
        return self._router.get_section_resume_url(self._routing_path)

    def can_display_summary(self):
        return self._router.can_display_section_summary(
            self._section_id, self._list_item_id
        )

    def _is_valid_location(self):
        return self._section_id in self._router.enabled_section_ids
