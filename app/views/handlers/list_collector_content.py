from app.views.handlers.list_collector import ListCollector


class ListCollectorContent(ListCollector):
    def _get_additional_view_context(self) -> dict:
        return self.rendered_block["content"]

    def handle_post(self):
        self._set_started_at_metadata()
        self.questionnaire_store_updater.add_completed_location()
        if self._is_list_collector_complete():
            self._update_section_completeness()
        self.questionnaire_store_updater.update_progress_for_dependent_sections()
        self.questionnaire_store_updater.save()
