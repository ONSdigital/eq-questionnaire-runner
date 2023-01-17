from app.views.contexts.summary.preview_question import PreviewQuestion


class PreviewBlock:
    def __init__(
        self,
        block_schema,
    ):
        self.title = block_schema.get("title")
        self.question = self.get_question(
            block_schema=block_schema,
        )

    @staticmethod
    def get_question(
        block_schema,
    ):

        return PreviewQuestion(
            block_schema.get("question_variants") or block_schema.get("question")
        ).serialize()

    def serialize(self):

        return {
            "title": self.title,
            "question": self.question,
        }
