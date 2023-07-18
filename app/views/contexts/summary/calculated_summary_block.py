from decimal import Decimal
from typing import Iterable, Mapping, MutableMapping, TypeAlias

from flask import url_for

from app.data_models import (
    AnswerStore,
    ListStore,
    ProgressStore,
    SupplementaryDataStore,
)
from app.data_models.metadata_proxy import MetadataProxy
from app.questionnaire import Location, QuestionnaireSchema
from app.questionnaire.rules.rule_evaluator import RuleEvaluator

NumericType: TypeAlias = int | float | Decimal


class CalculatedSummaryBlock:
    def __init__(
        self,
        block_schema: Mapping,
        *,
        answer_store: AnswerStore,
        list_store: ListStore,
        metadata: MetadataProxy | None,
        response_metadata: MutableMapping,
        schema: QuestionnaireSchema,
        location: Location,
        return_to: str | None,
        return_to_block_id: str | None = None,
        progress_store: ProgressStore,
        routing_path_block_ids: Iterable[str],
        supplementary_data_store: SupplementaryDataStore,
    ) -> None:
        """
        A Calculated summary block that is rendered as part of a grand calculated summary
        """

        self.id = block_schema["id"]
        self.title = block_schema["calculation"]["title"]
        self._return_to = return_to
        self._return_to_block_id = return_to_block_id
        self._block_schema = block_schema
        self._schema = schema

        self._rule_evaluator = RuleEvaluator(
            schema=schema,
            answer_store=answer_store,
            list_store=list_store,
            metadata=metadata,
            response_metadata=response_metadata,
            location=location,
            progress_store=progress_store,
            routing_path_block_ids=routing_path_block_ids,
            supplementary_data_store=supplementary_data_store,
        )

        # Type ignore: for a calculated summary the resolved answer would only ever be one of these 3
        calculated_total: NumericType = self._rule_evaluator.evaluate(block_schema["calculation"]["operation"])  # type: ignore
        answer_format = self._schema.get_answer_format_for_calculated_summary(self.id)
        self.answers = [
            {
                "id": self.id,
                "label": self.title,
                "value": calculated_total,
                "link": self._build_link(),
                **answer_format,
            }
        ]

    def _build_link(self) -> str:
        return url_for(
            "questionnaire.block",
            block_id=self.id,
            return_to=self._return_to,
            return_to_answer_id=self.id,
            return_to_block_id=self._return_to_block_id,
            _anchor=self.id,
        )

    def _calculated_summary(self) -> dict:
        return {"id": self.id, "title": self.title, "answers": self.answers}

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "calculated_summary": self._calculated_summary(),
        }
