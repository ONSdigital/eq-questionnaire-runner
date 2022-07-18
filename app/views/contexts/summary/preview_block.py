from typing import Optional

from app.questionnaire.rules.rule_evaluator import RuleEvaluator
from app.questionnaire.value_source_resolver import ValueSourceResolver
from app.questionnaire.variants import choose_variant
from app.views.contexts.summary.preview_question import PreviewQuestion


class PreviewBlock:
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
        return_to_block_id: Optional[str] = None,
    ):
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
        """ Taking question variants into account, return the question which was displayed to the user """

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
        return PreviewQuestion(
            variant,
            schema=schema,
            rule_evaluator=self._rule_evaluator,
            value_source_resolver=self._value_source_resolver,
            location=location,
        ).serialize()

    def serialize(self):

        return {
            "id": self.id,
            "title": self.title,
            "number": self.number,
            "question": self.question,
        }
