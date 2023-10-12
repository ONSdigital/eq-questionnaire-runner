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
from app.questionnaire import QuestionnaireSchema
from app.questionnaire.return_location import ReturnLocation
from app.questionnaire.rules.rule_evaluator import RuleEvaluator
from app.utilities.types import LocationType

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
        location: LocationType,
        return_location: ReturnLocation,
        progress_store: ProgressStore,
        routing_path_block_ids: Iterable[str],
        supplementary_data_store: SupplementaryDataStore,
    ) -> None:
        """
        A Calculated summary block that is rendered as part of a grand calculated summary

        If the GCS is in a repeating section, and the calculated summary also is
        then the list name and item id need to be used to build the calculated summary change link
        but if the GCS is repeating and the CS is not, the list parameters in the change link should be set to None
        """

        self.id = block_schema["id"]
        self.title = block_schema["calculation"]["title"]
        self._return_location = return_location
        self._block_schema = block_schema
        self._schema = schema
        if self._schema.is_block_in_repeating_section(self.id):
            self._list_item_id = location.list_item_id
            self._list_name = location.list_name
        else:
            self._list_item_id = None
            self._list_name = None

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
        # not required if the calculated summary is in the repeat alongside the GCS
        return_to_list_item_id = (
            self._return_location.return_to_list_item_id if not self._list_item_id else None
        )
        return url_for(     # TODO: Uses the self.id - move to return_location class still?
            "questionnaire.block",
            block_id=self.id,
            list_name=self._list_name,
            list_item_id=self._list_item_id,
            return_to=self._return_location.return_to,
            return_to_answer_id=self.id,
            return_to_block_id=self._return_location.return_to_block_id,
            return_to_list_item_id=return_to_list_item_id,
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
