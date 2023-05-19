from typing import Type

from app.views.contexts import GrandCalculatedSummaryContext
from app.views.contexts.calculated_summary_context import CalculatedSummaryContext
from app.views.handlers.content import Content


class _SummaryWithCalculation(Content):
    summary_class: Type[CalculatedSummaryContext] | Type[GrandCalculatedSummaryContext]

    def get_context(self):
        summary_context = self.summary_class(
            language=self._language,
            schema=self._schema,
            answer_store=self._questionnaire_store.answer_store,
            list_store=self._questionnaire_store.list_store,
            progress_store=self._questionnaire_store.progress_store,
            metadata=self._questionnaire_store.metadata,
            response_metadata=self._questionnaire_store.response_metadata,
            current_location=self._current_location,
            routing_path=self._routing_path,
            return_to=self.return_to,
            return_to_block_id=self.return_to_block_id,
        )
        context = summary_context.build_view_context()

        if not self.page_title:
            self.page_title = context["summary"]["calculated_question"]["title"]

        return context


class CalculatedSummary(_SummaryWithCalculation):
    summary_class = CalculatedSummaryContext


class GrandCalculatedSummary(_SummaryWithCalculation):
    summary_class = GrandCalculatedSummaryContext
