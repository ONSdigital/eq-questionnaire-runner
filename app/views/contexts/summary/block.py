from typing import Mapping, MutableMapping

from jsonpointer import resolve_pointer

from app.data_models import (
    AnswerStore,
    ListStore,
    ProgressStore,
    SupplementaryDataStore,
)
from app.data_models.metadata_proxy import MetadataProxy
from app.data_models.questionnaire_store import DataStores
from app.questionnaire import QuestionnaireSchema
from app.questionnaire.schema_utils import find_pointers_containing
from app.questionnaire.variants import choose_variant
from app.utilities.types import LocationType
from app.views.contexts.summary.question import Question


class Block:
    def __init__(
        self,
        block_schema: Mapping,
        *,
        data_stores: DataStores,
        schema: QuestionnaireSchema,
        location: LocationType,
        return_to: str | None,
        return_to_block_id: str | None = None,
        return_to_list_item_id: str | None = None,
        language: str,
    ) -> None:
        self.id = block_schema["id"]
        self.title = block_schema.get("title")
        self.number = block_schema.get("number")
        self.location = location
        self.schema = schema
        self.data_stores = data_stores

        self._rule_evaluator = self.data_stores.rule_evaluator(
            # Type ignore: location in rule_evaluator can be both Location or RelationshipLocation type but is only Location type here
            schema=self.schema,
            location=self.location,  # type: ignore
        )

        self._value_source_resolver = self.data_stores.value_source_resolver(
            schema=self.schema,
            location=self.location,
            list_item_id=self.location.list_item_id if self.location else None,
        )

        self.question = self.get_question(
            block_schema=block_schema,
            data_stores=self.data_stores,
            return_to=return_to,
            return_to_block_id=return_to_block_id,
            return_to_list_item_id=return_to_list_item_id,
            language=language,
        )

    def get_question(
        self,
        *,
        data_stores,
        block_schema: Mapping,
        return_to: str | None,
        return_to_block_id: str | None,
        return_to_list_item_id: str | None,
        language: str,
    ) -> dict[str, Question]:
        """Taking question variants into account, return the question which was displayed to the user"""

        variant = choose_variant(
            block_schema,
            self.schema,
            data_stores.metadata,
            data_stores.response_metadata,
            data_stores.answer_store,
            data_stores.list_store,
            variants_key="question_variants",
            single_key="question",
            current_location=self.location,
            progress_store=data_stores.progress_store,
            supplementary_data_store=data_stores.supplementary_data_store,
        )
        return Question(
            variant,
            answer_store=data_stores.answer_store,
            list_store=data_stores.list_store,
            progress_store=data_stores.progress_store,
            supplementary_data_store=data_stores.supplementary_data_store,
            schema=self.schema,
            rule_evaluator=self._rule_evaluator,
            value_source_resolver=self._value_source_resolver,
            location=self.location,
            block_id=self.id,
            return_to=return_to,
            return_to_block_id=return_to_block_id,
            return_to_list_item_id=return_to_list_item_id,
            metadata=data_stores.metadata,
            response_metadata=data_stores.response_metadata,
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
