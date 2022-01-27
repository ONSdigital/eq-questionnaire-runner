from flask import url_for
from app.questionnaire.questionnaire_schema import QuestionnaireSchema

from app.questionnaire.variants import choose_variant
from app.views.contexts.summary.question import Question


class Block:
    def __init__(
        self,
        block_schema,
        answer_store,
        list_store,
        metadata,
        response_metadata,
        schema: QuestionnaireSchema,
        location,
        return_to,
    ):
        self.id = block_schema["id"]
        self.location = location
        self.title = block_schema.get("title")
        self.number = block_schema.get("number")
        first_answer_id_for_block = schema.get_answer_ids_for_block(self.id)[0]
        self.link = self._build_link(
            block_schema["id"], return_to, first_answer_id_for_block
        )
        self.question = self.get_question(
            block_schema,
            answer_store,
            list_store,
            metadata,
            response_metadata,
            schema,
            location,
        )

    def _build_link(self, block_id, return_to, return_to_answer_id):
        return url_for(
            "questionnaire.block",
            list_name=self.location.list_name,
            block_id=block_id,
            list_item_id=self.location.list_item_id,
            return_to=return_to,
            return_to_answer_id=return_to_answer_id,
        )

    @staticmethod
    def get_question(
        block_schema,
        answer_store,
        list_store,
        metadata,
        response_metadata,
        schema,
        location,
    ):
        """ Taking question variants into account, return the question which was displayed to the user """
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

        return Question(variant, answer_store, schema, list_item_id).serialize()

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "number": self.number,
            "link": self.link,
            "question": self.question,
        }
