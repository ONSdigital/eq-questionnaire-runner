from app.views.handlers.content import Content
from app.views.contexts import CustomSectionSummaryContext, SectionSummaryContext


class SectionSummary(Content):
    @property
    def rendered_block(self):
        return self._render_block(self.block["id"])

    def get_context(self):
        section_id = self._schema.get_section_id_for_block_id(self.block["id"])

        if not self._schema.get_summary_for_section(section_id):
            section_summary_context = SectionSummaryContext
        else:
            section_summary_context = CustomSectionSummaryContext

        section_summary_context = section_summary_context(
            self._language,
            self._schema,
            self._questionnaire_store.answer_store,
            self._questionnaire_store.list_store,
            self._questionnaire_store.progress_store,
            self._questionnaire_store.metadata,
        )

        return section_summary_context(self._current_location)
