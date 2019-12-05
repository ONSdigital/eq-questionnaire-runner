from app.views.contexts.calculated_summary import (
    build_view_context_for_calculated_summary,
)
from app.views.handlers.content import Content


class CalculatedSummary(Content):
    def get_context(self):
        return build_view_context_for_calculated_summary(
            self._language,
            self._current_location,
            self._schema,
            self._questionnaire_store.answer_store,
            self._questionnaire_store.progress_store,
            self._questionnaire_store.list_store,
            self._questionnaire_store.metadata,
        )
