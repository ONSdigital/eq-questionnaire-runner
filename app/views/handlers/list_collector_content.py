from typing import Any

from app.views.handlers.list_collector import ListCollector
from app.views.handlers.question import Question


class ListCollectorContent(ListCollector):
    def _get_additional_view_context(self) -> Any:
        return self.rendered_block["content"]

    def handle_post(self) -> None:
        if self._is_list_collector_complete():
            self._routing_path = self.router.routing_path(
                section_id=self._current_location.section_id,
                list_item_id=self._current_location.list_item_id,
            )
            return super(Question, self).handle_post()
        self.questionnaire_store_updater.add_completed_location()
        self.questionnaire_store_updater.update_progress_for_dependent_sections()
        self.questionnaire_store_updater.save()
