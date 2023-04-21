from typing import Any, Mapping, Optional

from app.data_models import AnswerStore, ListStore, ProgressStore
from app.data_models.metadata_proxy import MetadataProxy
from app.questionnaire import Location, QuestionnaireSchema
from app.questionnaire.rules.rule_evaluator import RuleEvaluator
from app.questionnaire.value_source_resolver import ValueSourceResolver
from app.views.contexts.summary.block import Block
from app.views.contexts.summary.calculated_summary import CalculatedSummary


class CalculatedSummaryBlock:
    def __init__(
        self,
        block_schema: Mapping[str, Any],
        *,
        answer_store: AnswerStore,
        list_store: ListStore,
        metadata: Optional[MetadataProxy],
        response_metadata: Mapping,
        schema: QuestionnaireSchema,
        location: Location,
        return_to: Optional[str],
        return_to_block_id: Optional[str] = None,
        progress_store: ProgressStore,
        answer_format: Mapping | None = None,
    ) -> None:
        self.id = block_schema["id"]
        self.title = block_schema.get("title")
        self.number = block_schema.get("number")
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

        self._value_source_resolver = ValueSourceResolver(
            answer_store=answer_store,
            list_store=list_store,
            metadata=metadata,
            response_metadata=response_metadata,
            schema=schema,
            location=location,
            list_item_id=location.list_item_id if location else None,
            use_default_answer=True,
            progress_store=progress_store,
        )

        self._calculated_summary = CalculatedSummary(
            block_id=self.id,
            return_to=self.return_to,
            return_to_block_id=self.return_to_block_id,
            # answers must be in this form
            # {
            #     "id": "hack_answer",
            #     "label": "Hack label",
            #     "value": 1,
            #     "type": "currency",
            #     "unit": None,
            #     "unit_length": None,
            #     "currency": "GBP",
            #     "link": "google.com",
            # }
            answers=[],
        ).serialize()

    def evaluate_calculated_summary(self):
        calculation = self.block_schema.get("calculation")
        total = self._rule_evaluator.evaluate(calculation)
        formatted_total = self._format_total(self.answer_format, total)
        return formatted_total

    def serialize(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "number": self.number,
            "calculated_summary": self._calculated_summary,
        }
