from typing import Mapping, MutableMapping

from jsonpointer import resolve_pointer

from app.data_models import AnswerStore, ListStore, ProgressStore
from app.data_models.metadata_proxy import MetadataProxy
from app.questionnaire import Location, QuestionnaireSchema
from app.questionnaire.rules.rule_evaluator import RuleEvaluator
from app.questionnaire.schema_utils import find_pointers_containing
from app.questionnaire.value_source_resolver import ValueSourceResolver
from app.questionnaire.variants import choose_variant
from app.views.contexts.summary.question import Question


class Block:
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
        language: str,
    ) -> None:
        self.id = block_schema["id"]
        self.title = block_schema.get("title")
        self.number = block_schema.get("number")
        self.location = location
        self.schema = schema

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
            return_to=return_to,
            return_to_block_id=return_to_block_id,
            progress_store=progress_store,
            language=language,
        )

    def get_question(
        self,
        *,
        block_schema: Mapping,
        answer_store: AnswerStore,
        list_store: ListStore,
        metadata: MetadataProxy | None,
        response_metadata: MutableMapping,
        return_to: str | None,
        return_to_block_id: str | None,
        progress_store: ProgressStore,
        language: str,
    ) -> dict[str, Question]:
        """Taking question variants into account, return the question which was displayed to the user"""

        variant = choose_variant(
            block_schema,
            self.schema,
            metadata,
            response_metadata,
            answer_store,
            list_store,
            variants_key="question_variants",
            single_key="question",
            current_location=self.location,
            progress_store=progress_store,
        )
        return Question(
            variant,
            answer_store=answer_store,
            list_store=list_store,
            progress_store=progress_store,
            schema=self.schema,
            rule_evaluator=self._rule_evaluator,
            value_source_resolver=self._value_source_resolver,
            location=self.location,
            block_id=self.id,
            return_to=return_to,
            return_to_block_id=return_to_block_id,
            metadata=metadata,
            response_metadata=response_metadata,
            language=language,
        ).serialize()

    def _handle_id_suffixing(self, block: dict) -> dict:
        """
        If the block is repeating but not within a repeating section, summary pages will render it multiple times, once per list item
        so the block id, as well as any other ids (e.g. question, answer) need suffixing with list_item_id to ensure the HTML rendered is valid and doesn't
        have duplicate div ids
        """
        if (
            self.location.list_item_id
            and not self.schema.is_block_in_repeating_section(self.id)
        ):
            for pointer in find_pointers_containing(block, "id"):
                data = resolve_pointer(block, pointer)
                data["id"] = f"{data['id']}-{self.location.list_item_id}"
        return block

    def serialize(self) -> dict:
        return self._handle_id_suffixing(
            {
                "id": self.id,
                "title": self.title,
                "number": self.number,
                "question": self.question,
            }
        )
