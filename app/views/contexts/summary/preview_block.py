from app.questionnaire.variants import choose_variant
from app.views.contexts.summary.preview_question import PreviewQuestion


class PreviewBlock:
    def __init__(
        self,
        block_schema,
        *,
        schema,
    ):
        self.id = block_schema["id"]
        self.title = block_schema.get("title")
        self.number = block_schema.get("number")

        self.question = self.get_question(
            block_schema=block_schema,
            answer_store={},
            list_store={},
            metadata={},
            response_metadata={},
            schema=schema,
            location=None,
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
        return PreviewQuestion(variant, schema=schema).serialize()

    def serialize(self):

        return {
            "id": self.id,
            "title": self.title,
            "number": self.number,
            "question": self.question,
        }
