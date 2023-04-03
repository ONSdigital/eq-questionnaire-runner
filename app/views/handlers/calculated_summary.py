from app.views.contexts.calculated_summary_context import CalculatedSummaryContext
from app.views.handlers.content import Content


class CalculatedSummary(Content):
    def get_context(self):
        calculated_summary_context = CalculatedSummaryContext(
            language=self._language,
            schema=self._schema,
            answer_store=self._questionnaire_store.answer_store,
            list_store=self._questionnaire_store.list_store,
            progress_store=self._questionnaire_store.progress_store,
            metadata=self._questionnaire_store.metadata,
            response_metadata=self._questionnaire_store.response_metadata,
            current_location=self._current_location,
            routing_path=self._routing_path,
        )
        context = calculated_summary_context.build_view_context_for_calculated_summary()

        if not self.page_title:
            self.page_title = context["summary"]["calculated_question"]["title"]

        return context

    def handle_post(self):
        # We prematurely set the current as complete, so that dependent sections can be updated accordingly
        self.questionnaire_store_updater.add_completed_location()
        # Then we update dependent sections
        self.questionnaire_store_updater.complete_calculated_summary_block()
        return super().handle_post()
