from app.views.contexts.list_collector_summary_context import (
    ListCollectorSummaryContext,
)
from app.views.handlers.content import Content


class ListCollectorSummary(Content):
    def get_context(self):
        summary_context = ListCollectorSummaryContext(
            self._language,
            self._schema,
            self._questionnaire_store.answer_store,
            self._questionnaire_store.list_store,
            self._questionnaire_store.progress_store,
            self._questionnaire_store.metadata,
        )
        return summary_context.build_view_context(self._current_location)
