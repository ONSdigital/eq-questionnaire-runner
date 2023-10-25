from typing import Mapping

from jsonpointer import resolve_pointer

from app.data_models.data_stores import DataStores
from app.questionnaire import QuestionnaireSchema
from app.questionnaire.return_location import ReturnLocation
from app.questionnaire.rules.rule_evaluator import RuleEvaluator
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
        return_location: ReturnLocation,
        language: str,
    ) -> None:
        self.id = block_schema["id"]
        self.title = block_schema.get("title")
        self.number = block_schema.get("number")
        self.location = location
        self.schema = schema
        self.data_stores = data_stores

        self.question = self.get_question(
            block_schema=block_schema,
            data_stores=self.data_stores,
            return_location=return_location,
            language=language,
        )

    def get_question(
        self,
        *,
        data_stores: DataStores,
        block_schema: Mapping,
        return_location: ReturnLocation,
        language: str,
    ) -> dict[str, Question]:
        """Taking question variants into account, return the question which was displayed to the user"""

        variant = choose_variant(
            block_schema,
            self.schema,
            data_stores,
            variants_key="question_variants",
            single_key="question",
            current_location=self.location,
        )
        return Question(
            variant,
            data_stores=self.data_stores,
            schema=self.schema,
            location=self.location,
            block_id=self.id,
            return_location=return_location,
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
