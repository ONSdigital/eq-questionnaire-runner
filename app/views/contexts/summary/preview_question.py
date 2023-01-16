class PreviewQuestion:
    def __init__(
        self,
        question_schema,
        *,
        schema,
    ):
        self.id = question_schema["id"]
        self.type = question_schema["type"]
        self.schema = schema
        self.summary = question_schema.get("summary")
        self.title = (
            question_schema.get("title") or question_schema["answers"][0]["label"]
        )

        self.answers = self._build_answers(question_schema)
        self.descriptions = self._build_descriptions(question_schema)
        self.guidance = self._build_question_guidance(question_schema)
        self.text_length = self._get_length(question_schema)
        self.instruction = self._build_instruction(question_schema)
        self.answer_description = self._build_answer_descriptions(
            iter(question_schema["answers"])
        )
        self.answer_guidance = self._build_answer_guidance(
            answers=iter(question_schema["answers"])
        )

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

    @staticmethod
    def _build_descriptions(question_schema):
        if description := question_schema.get("description"):

            return description

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
        question_schema,
    ):
        if answers := question_schema.get("answers"):
            for answer in answers:
                if answer.get("type") == "TextArea":
                    return answer.get("max_length")

        return None

    @staticmethod
    def _build_instruction(question_schema):
        if instruction := question_schema.get("instruction"):
            return instruction
        return None

    def serialize(self):
        return {
            "id": self.id,
            "type": self.type,
            "title": self.title,
            "answers": self.answers,
            "descriptions": self.descriptions,
            "guidance": self.guidance,
            "text_length": self.text_length,
            "instruction": self.instruction,
            "answer_description": self.answer_description,
            "answer_guidance": self.answer_guidance,
        }
