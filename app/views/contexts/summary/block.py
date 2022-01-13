from flask import url_for

from app.questionnaire.rules.rule_evaluator import RuleEvaluator
from app.questionnaire.schema_utils import choose_variant
from app.views.contexts.summary.question import Question


class Block:
    def __init__(
        self,
        block_schema,
        *,
        answer_store,
        list_store,
        metadata,
        response_metadata,
        schema,
        location,
        return_to,
    ):
        self.id = block_schema["id"]
        self.location = location
        self.title = block_schema.get("title")
        self.number = block_schema.get("number")
        self.link = self._build_link(block_schema["id"], return_to)

        self._rule_evaluator = RuleEvaluator(
            schema=schema,
            answer_store=answer_store,
            list_store=list_store,
            metadata=metadata,
            response_metadata=response_metadata,
            location=location,
        )

        self.question = self.get_question(
            block_schema=block_schema,
            answer_store=answer_store,
            list_store=list_store,
            metadata=metadata,
            response_metadata=response_metadata,
            schema=schema,
            location=location,
        )

    def _build_link(self, block_id, return_to):
        return url_for(
            "questionnaire.block",
            list_name=self.location.list_name,
            block_id=block_id,
            list_item_id=self.location.list_item_id,
            return_to=return_to,
        )

    def get_question(
        self,
        *,
        block_schema,
        answer_store,
        list_store,
        metadata,
        response_metadata,
        schema,
        location,
    ):
        """Taking question variants into account, return the question which was displayed to the user"""
        list_item_id = location.list_item_id

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
        )

        return Question(
            variant,
            answer_store=answer_store,
            schema=schema,
            list_item_id=list_item_id,
            rule_evaluator=self._rule_evaluator,
        ).serialize()

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "number": self.number,
            "link": self.link,
            "question": self.question,
        }
