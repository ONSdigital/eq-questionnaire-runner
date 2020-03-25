from app.views.contexts import QuestionnaireSummaryContext
from app.views.handlers.content import Content


class Summary(Content):
    def get_context(self):
        questionnaire_summary_context = QuestionnaireSummaryContext(
            self._language,
            self._schema,
            self._questionnaire_store.answer_store,
            self._questionnaire_store.list_store,
            self._questionnaire_store.progress_store,
            self._questionnaire_store.metadata,
        )
        block = self._schema.get_block(self._current_location.block_id)
        collapsible = block.get("collapsible", False)
        is_view_submitted_response_enabled = {
            "is_view_submission_response_enabled": self._schema.is_view_submitted_response_enabled()
        }
        context = questionnaire_summary_context(collapsible)
        context["summary"].update(is_view_submitted_response_enabled)
        return context
