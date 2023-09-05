from app.questionnaire.location import SectionKey
from app.views.handlers.list_collector import ListCollector
from app.views.handlers.question import Question


class ListCollectorContent(ListCollector):
    def _get_additional_view_context(self) -> dict:
        return self.rendered_block.get("content", {})

    def handle_post(self) -> None:
        if self._is_list_collector_complete():
            self._routing_path = self.router.routing_path(
                SectionKey(
                    section_id=self._current_location.section_id,
                    list_item_id=self._current_location.list_item_id,
                )
            )
            return super(Question, self).handle_post()
