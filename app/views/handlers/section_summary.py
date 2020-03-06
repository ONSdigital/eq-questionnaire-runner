from app.views.handlers.content import Content
from app.views.contexts import SectionSummaryContext


class SectionSummary(Content):
    @property
    def rendered_block(self):
        return self._render_block(self.block["id"])

    def get_context(self):
        section_summary_context = SectionSummaryContext(
            self._language,
            self._schema,
            self._questionnaire_store.answer_store,
            self._questionnaire_store.list_store,
            self._questionnaire_store.progress_store,
            self._questionnaire_store.metadata,
        )

        return section_summary_context(self._current_location)
