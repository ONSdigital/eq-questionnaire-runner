from re import findall

from app.questionnaire import QuestionnaireSchema


class PreviewQuestion:
    def __init__(self, question_schema, survey_data):
        self.title = question_schema.get("title")
        self.answers = self._build_answers(question_schema)
        self.descriptions = self._build_descriptions(question_schema, survey_data)
        self.guidance = self._build_question_guidance(question_schema)
        self.text_length = self._get_length(question_schema.get("answers"))
        self.instruction = question_schema.get("instruction") or None
        self.answer_description = self._build_answer_descriptions(
            iter(question_schema["answers"])
        )
        self.answer_guidance = self._build_answer_guidance(
            answers=iter(question_schema["answers"])
        )
        self.survey_data = survey_data

    @staticmethod
    def _build_answers(question_schema):
        answers = []
        for answer in iter(question_schema["answers"]):
            if options := answer.get("options"):
                answers.extend(option["label"] for option in options)
            if not options:
                answers.append(answer["label"])

        return answers

    @staticmethod
    def _build_answer_descriptions(answers):
        return next(
            (
                answer.get("description")
                for answer in answers
                if answer.get("description")
            ),
            None,
        )

    def _build_answer_guidance(self, answers):
        for answer in answers:
            return self._build_guidance(answer)

    def _build_descriptions(self, question_schema, survey_data):
        if descriptions := question_schema.get("description"):
            mutable_descriptions = QuestionnaireSchema.get_mutable_deepcopy(
                descriptions
            )
            for index, _ in enumerate(mutable_descriptions):
                if isinstance(mutable_descriptions[index], dict):
                    mutable_descriptions[index] = self.resolve_text(
                        mutable_descriptions[index], survey_data
                    )

            return mutable_descriptions

        return None

    def _build_question_guidance(self, question_schema):
        return self._build_guidance(question_schema)

    @staticmethod
    def _build_guidance(schema_element):
        if guidance := schema_element.get("guidance"):
            guidance_list = []
            for contents in guidance.get("contents"):
                if contents.get("description"):
                    guidance_list.append(contents.get("description"))
                elif contents.get("list"):
                    guidance_items = list(contents.get("list"))
                    guidance_list.append(guidance_items)
            return guidance_list
        return None

    @staticmethod
    def _get_length(
        answers,
    ):
        return next(
            (
                answer.get("max_length")
                for answer in answers
                if answer.get("type") == "TextArea"
            ),
            None,
        )

    def serialize(self):
        return {
            "title": self.title,
            "answers": self.answers,
            "descriptions": self.descriptions,
            "guidance": self.guidance,
            "text_length": self.text_length,
            "instruction": self.instruction,
            "answer_description": self.answer_description,
            "answer_guidance": self.answer_guidance,
        }

    @staticmethod
    def resolve_text(description, survey_data):
        placeholders = findall(r"\{.*?}", description.get("text"))

        text = description.get("text")

        for placeholder in placeholders:
            stripped_placeholder = placeholder.replace("{", "").replace("}", "")
            if stripped_placeholder in survey_data:
                text = text.replace(placeholder, survey_data[stripped_placeholder])

        description = text

        return description
