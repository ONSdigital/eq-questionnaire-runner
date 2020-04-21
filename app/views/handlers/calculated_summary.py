from app.views.contexts.calculated_summary_context import CalculatedSummaryContext
from app.views.handlers.content import Content


class CalculatedSummary(Content):
    def get_context(self):
        calculated_summary_context = CalculatedSummaryContext(
            self._language,
            self._schema,
            self._questionnaire_store.answer_store,
            self._questionnaire_store.list_store,
            self._questionnaire_store.progress_store,
            self._questionnaire_store.metadata,
        )
        return calculated_summary_context.build_view_context_for_calculated_summary(
            self._current_location
        )
