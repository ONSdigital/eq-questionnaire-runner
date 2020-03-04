from app.views.contexts import FinalSummaryContext
from app.views.handlers.content import Content


class Summary(Content):
    def get_context(self):
        final_summary_context = FinalSummaryContext(
            self._language,
            self._schema,
            self._questionnaire_store.answer_store,
            self._questionnaire_store.list_store,
            self._questionnaire_store.progress_store,
            self._questionnaire_store.metadata,
        )
        collapsible = self._schema.get_block(self._current_location.block_id).get(
            "collapsible", False
        )
        return final_summary_context(collapsible)
