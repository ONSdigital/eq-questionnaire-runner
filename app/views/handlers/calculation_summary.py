from app.views.contexts import GrandCalculatedSummaryContext
from app.views.contexts.calculated_summary_context import CalculatedSummaryContext
from app.views.handlers.content import Content


class _SummaryWithCalculation(Content):
    summary_class: type[CalculatedSummaryContext] | type[GrandCalculatedSummaryContext]

    def get_context(self) -> dict[str, dict]:
        summary_context = self.summary_class(
            language=self._language,
            schema=self._schema,
            data_stores=self._questionnaire_store.data_stores,
            current_location=self._current_location,
            routing_path=self._routing_path,
            return_location=self._return_location,
            rendered_block=self.rendered_block,
        )
        context = summary_context.build_view_context()

        if not self.page_title:
            self.page_title = context["summary"]["calculated_question"]["title"]

        return context

    def handle_post(self) -> None:
        # We prematurely set the current as complete, so that dependent sections can be updated accordingly
        self.questionnaire_store_updater.add_completed_location(self.current_location)
        # Then we update dependent sections
        self.questionnaire_store_updater.capture_progress_section_dependencies()
        return super().handle_post()


class CalculatedSummary(_SummaryWithCalculation):
    summary_class = CalculatedSummaryContext


class GrandCalculatedSummary(_SummaryWithCalculation):
    summary_class = GrandCalculatedSummaryContext
