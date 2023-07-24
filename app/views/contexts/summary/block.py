from typing import Any, Mapping, MutableMapping, Optional

from app.data_models import AnswerStore, ListStore, ProgressStore
from app.data_models.metadata_proxy import MetadataProxy
from app.questionnaire import QuestionnaireSchema
from app.questionnaire.rules.rule_evaluator import RuleEvaluator
from app.questionnaire.value_source_resolver import ValueSourceResolver
from app.questionnaire.variants import choose_variant
from app.utilities.types import LocationType
from app.views.contexts.summary.question import Question


class Block:
    def __init__(
        self,
        block_schema: Mapping[str, Any],
        *,
        answer_store: AnswerStore,
        list_store: ListStore,
        metadata: Optional[MetadataProxy],
        response_metadata: MutableMapping,
        schema: QuestionnaireSchema,
        location: LocationType,
        return_to: Optional[str],
        return_to_block_id: Optional[str] = None,
        progress_store: ProgressStore,
        language: str,
    ) -> None:
        self.id = block_schema["id"]
        self.title = block_schema.get("title")
        self.number = block_schema.get("number")

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

        self.question = self.get_question(
            block_schema=block_schema,
            answer_store=answer_store,
            list_store=list_store,
            metadata=metadata,
            response_metadata=response_metadata,
            schema=schema,
            location=location,
            return_to=return_to,
            return_to_block_id=return_to_block_id,
            progress_store=progress_store,
            language=language,
        )

    def get_question(
        self,
        *,
        block_schema: Mapping[str, Any],
        answer_store: AnswerStore,
        list_store: ListStore,
        metadata: Optional[MetadataProxy],
        response_metadata: MutableMapping,
        schema: QuestionnaireSchema,
        location: LocationType,
        return_to: Optional[str],
        return_to_block_id: Optional[str],
        progress_store: ProgressStore,
        language: str,
    ) -> dict[str, Question]:
        """Taking question variants into account, return the question which was displayed to the user"""

        variant = choose_variant(
            block_schema,
            schema,
            metadata,
            response_metadata,
            answer_store,
            list_store,
            variants_key="question_variants",
            single_key="question",
            current_location=location,
            progress_store=progress_store,
        )
        return Question(
            variant,
            answer_store=answer_store,
            list_store=list_store,
            progress_store=progress_store,
            schema=schema,
            rule_evaluator=self._rule_evaluator,
            value_source_resolver=self._value_source_resolver,
            location=location,
            block_id=self.id,
            return_to=return_to,
            return_to_block_id=return_to_block_id,
            metadata=metadata,
            response_metadata=response_metadata,
            language=language,
        ).serialize()

    def serialize(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "number": self.number,
            "question": self.question,
        }
