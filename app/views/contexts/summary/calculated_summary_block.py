from decimal import Decimal
from typing import Any, Mapping

from app.data_models import AnswerStore, ListStore, ProgressStore
from app.data_models.metadata_proxy import MetadataProxy
from app.questionnaire import Location, QuestionnaireSchema
from app.questionnaire.rules.rule_evaluator import RuleEvaluator
from app.views.contexts.summary.calculated_summary import CalculatedSummary


class CalculatedSummaryBlock:
    def __init__(
        self,
        block_schema: Mapping[str, Any],
        *,
        answer_store: AnswerStore,
        list_store: ListStore,
        metadata: MetadataProxy | None,
        response_metadata: Mapping,
        schema: QuestionnaireSchema,
        location: Location,
        return_to: str | None,
        return_to_block_id: str | None = None,
        progress_store: ProgressStore,
        answer_format: Mapping,
    ) -> None:
        self.id = block_schema["id"]
        self.title = block_schema["calculation"].get("title")
        self.return_to = return_to
        self.return_to_block_id = return_to_block_id
        self.block_schema = block_schema
        self.answer_format = answer_format

        self._rule_evaluator = RuleEvaluator(
            schema=schema,
            answer_store=answer_store,
            list_store=list_store,
            metadata=metadata,
            response_metadata=response_metadata,
            location=location,
            progress_store=progress_store,
        )
        # Type ignore: for a calculated summary the resolved answer would only ever be one of these 3
        self._calculated_total: int | float | Decimal = self._rule_evaluator.evaluate(block_schema["calculation"]["operation"])  # type: ignore
        self._calculated_summary = CalculatedSummary(
            title=self.title,
            block_id=self.id,
            return_to=self.return_to,
            return_to_block_id=self.return_to_block_id,
            calculated_total=self._calculated_total,
            answer_format=answer_format,
        ).serialize()

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "calculated_summary": self._calculated_summary,
        }
