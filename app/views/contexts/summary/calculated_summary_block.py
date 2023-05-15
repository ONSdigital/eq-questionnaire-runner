from decimal import Decimal
from typing import Any, Iterable, Mapping, MutableMapping

from flask import url_for

from app.data_models import AnswerStore, ListStore, ProgressStore
from app.data_models.metadata_proxy import MetadataProxy
from app.questionnaire import Location, QuestionnaireSchema
from app.questionnaire.questionnaire_schema import get_calculated_summary_answer_ids
from app.questionnaire.rules.rule_evaluator import RuleEvaluator


class CalculatedSummaryBlock:
    def __init__(
        self,
        block_schema: Mapping[str, Any],
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
    ) -> None:
        """
        A Calculated summary block that is rendered as part of a grand calculated summary
        """

        self.id = block_schema["id"]
        self.title = block_schema["calculation"].get("title")
        self.return_to = return_to
        self.return_to_block_id = return_to_block_id
        self.location = location
        self.block_schema = block_schema
        self.schema = schema

        self._rule_evaluator = RuleEvaluator(
            schema=schema,
            answer_store=answer_store,
            list_store=list_store,
            metadata=metadata,
            response_metadata=response_metadata,
            location=location,
            progress_store=progress_store,
            routing_path_block_ids=routing_path_block_ids,
        )

        # Type ignore: for a calculated summary the resolved answer would only ever be one of these 3
        calculated_total: int | float | Decimal = self._rule_evaluator.evaluate(block_schema["calculation"]["operation"])  # type: ignore
        self.answers = [
            {
                "id": self.id,
                "label": self.title,
                "value": calculated_total,
                "link": self._build_link(),
                **self._get_answer_format(),
            }
        ]

    def _build_link(self) -> str:
        return url_for(
            "questionnaire.block",
            block_id=self.id,
            return_to=self.return_to,
            return_to_answer_id=self.id,
            return_to_block_id=self.return_to_block_id,
            _anchor=self.id,
        )

    def _get_answer_format(self) -> dict:
        # the format will be the same for all answers in calculated summary so can just take the first
        first_answer_id = get_calculated_summary_answer_ids(self.block_schema)[0]
        first_answer = self.schema.get_answers_by_answer_id(first_answer_id)[0]
        return {
            "type": first_answer["type"].lower(),
            "unit": first_answer.get("unit"),
            "unit_length": first_answer.get("unit_length"),
            "currency": first_answer.get("currency"),
        }

    def _calculated_summary(self) -> dict:
        return {"id": self.id, "title": self.title, "answers": self.answers}

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "calculated_summary": self._calculated_summary(),
        }