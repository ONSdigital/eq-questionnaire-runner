from app.views.handlers.list_collector import ListCollector
from app.views.handlers.question import Question


class ListCollectorContent(ListCollector):
    def _get_additional_view_context(self) -> dict:
        return dict(self.rendered_block.get("content", {}))

    def handle_post(self) -> None:
        if self._is_list_collector_complete():
            self._routing_path = self.router.routing_path(
                self._current_location.section_key
            )
            return super(Question, self).handle_post()
