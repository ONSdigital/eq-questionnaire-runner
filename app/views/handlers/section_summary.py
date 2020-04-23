import flask_babel
from flask import url_for

from app.views.contexts import SectionSummaryContext


class SectionSummary:
    def __init__(self, schema, questionnaire_store, current_location, router):
        self._schema = schema
        self._questionnaire_store = questionnaire_store
        self.current_location = current_location
        self._router = router
        self._section_id = current_location.section_id
        self._list_item_id = current_location.list_item_id
        self._routing_path = router.routing_path(
            section_id=self._section_id, list_item_id=self._list_item_id
        )
        self.page_title = schema.get_title_for_section(self.current_location.section_id)

    def can_access_section_summary(self):
        return self._schema.is_summary_in_section(
            self.current_location.section_id
        ) and self._questionnaire_store.progress_store.is_section_complete(
            self._section_id, self._list_item_id
        )

    def context(self):
        section_summary_context = SectionSummaryContext(
            flask_babel.get_locale().language,
            self._schema,
            self._questionnaire_store.answer_store,
            self._questionnaire_store.list_store,
            self._questionnaire_store.progress_store,
            self._questionnaire_store.metadata,
        )
        return section_summary_context(self.current_location)

    def get_next_location_url(self):
        if self._schema.is_hub_enabled():
            return url_for(".get_questionnaire")
        return self._router.get_first_incomplete_location_in_survey().url()

    def get_previous_location_url(self):
        return self._router.get_last_location_in_section(self._routing_path).url()
