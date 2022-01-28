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
        schema,
        location,
        return_to,
    ):
        self.id = block_schema["id"]
        self.location = location
        self.title = block_schema.get("title")
        self.number = block_schema.get("number")
        self.return_to = return_to
        self.question = self.get_question(
            block_schema,
            answer_store,
            list_store,
            metadata,
            response_metadata,
            schema,
            location,
        )

    def get_question(
        self,
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

        return Question(
            variant,
            answer_store,
            schema,
            location.list_item_id,
            self.id,
            location.list_name,
            self.return_to,
        ).serialize()

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "number": self.number,
            "question": self.question,
        }
