from dataclasses import dataclass, field
from typing import Iterable, MutableMapping

from ordered_set import OrderedSet

from app.data_models.answer_store import AnswerStore
from app.data_models.list_store import ListStore
from app.data_models.metadata_proxy import MetadataProxy
from app.data_models.progress_store import ProgressStore
from app.data_models.supplementary_data_store import SupplementaryDataStore
from app.questionnaire import (
    Location,
    QuestionnaireSchema,
    placeholder_renderer,
    value_source_resolver,
)
from app.questionnaire.relationship_location import RelationshipLocation
from app.questionnaire.rules import rule_evaluator
from app.utilities.types import LocationType


@dataclass
class DataStores:
    # self.metadata is a read-only view over self._metadata
    metadata: MetadataProxy | None = None
    response_metadata: MutableMapping = field(default_factory=dict)
    list_store: ListStore = field(default_factory=ListStore)
    answer_store: AnswerStore = field(default_factory=AnswerStore)
    progress_store: ProgressStore = field(default_factory=ProgressStore)
    supplementary_data_store: SupplementaryDataStore = field(
        default_factory=SupplementaryDataStore
    )

    def rule_evaluator(
        self,
        *,
        schema: QuestionnaireSchema,
        location: Location,
        routing_path_block_ids: Iterable[str] | None = None,
    ) -> rule_evaluator.RuleEvaluator:
        return rule_evaluator.RuleEvaluator(
            schema=schema,
            answer_store=self.answer_store,
            list_store=self.list_store,
            metadata=self.metadata,
            response_metadata=self.response_metadata,
            progress_store=self.progress_store,
            location=location,
            routing_path_block_ids=routing_path_block_ids,
            supplementary_data_store=self.supplementary_data_store,
        )

    def value_source_resolver(
        self,
        *,
        schema: QuestionnaireSchema,
        location: Location | RelationshipLocation | None,
        list_item_id: str | None,
        routing_path_block_ids: OrderedSet[str] | None = None,
        assess_routing_path: bool = True,
        use_default_answer: bool = True,
        escape_answer_values: bool = True,
    ) -> value_source_resolver.ValueSourceResolver:
        return value_source_resolver.ValueSourceResolver(
            answer_store=self.answer_store,
            list_store=self.list_store,
            metadata=self.metadata,
            schema=schema,
            location=location,
            list_item_id=list_item_id,
            escape_answer_values=escape_answer_values,
            response_metadata=self.response_metadata,
            use_default_answer=use_default_answer,
            assess_routing_path=assess_routing_path,
            routing_path_block_ids=routing_path_block_ids,
            progress_store=self.progress_store,
            supplementary_data_store=self.supplementary_data_store,
        )

    def placeholder_renderer(
        self,
        language: str,
        schema: QuestionnaireSchema,
        location: LocationType | None = None,
        placeholder_preview_mode: bool | None = False,
    ) -> placeholder_renderer.PlaceholderRenderer:
        return placeholder_renderer.PlaceholderRenderer(
            language=language,
            answer_store=self.answer_store,
            list_store=self.list_store,
            metadata=self.metadata,
            response_metadata=self.response_metadata,
            schema=schema,
            progress_store=self.progress_store,
            supplementary_data_store=self.supplementary_data_store,
            location=location,
            placeholder_preview_mode=placeholder_preview_mode,
        )
