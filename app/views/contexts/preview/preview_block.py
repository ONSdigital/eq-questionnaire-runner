from app.views.contexts.preview.preview_question import PreviewQuestion


class PreviewBlock:
    def __init__(self, block_schema, survey_data):
        self.survey_data = survey_data
        self.title = block_schema.get("title")
        self.question = self.get_question(
            block_schema=block_schema, survey_data=self.survey_data
        )

    @staticmethod
    def get_question(block_schema, survey_data):
        return PreviewQuestion(
            block_schema.get(
                "question",
            )
            or block_schema["question_variants"][0]["question"],
            survey_data,
        ).serialize()

    def serialize(self):

        return {
            "title": self.title,
            "question": self.question,
        }
