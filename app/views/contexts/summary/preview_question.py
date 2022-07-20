class PreviewQuestion:
    def __init__(
        self,
        question_schema,
        *,
        schema,
        rule_evaluator,
        value_source_resolver,
        location,
    ):
        self.list_item_id = location.list_item_id if location else None
        self.id = question_schema["id"]
        self.type = question_schema["type"]
        self.schema = schema
        self.answer_schemas = iter(question_schema["answers"])
        self.summary = question_schema.get("summary")
        self.title = (
            question_schema.get("title") or question_schema["answers"][0]["label"]
        )
        self.number = question_schema.get("number", None)

        self.rule_evaluator = rule_evaluator
        self.value_source_resolver = value_source_resolver

        self.answers = self._build_answers()
        self.descriptions = self._build_descriptions(question_schema=question_schema)
        self.guidance = self._build_guidance(question_schema=question_schema)
        self.text_length = self._get_length(question_schema=question_schema)
        self.instruction = self._build_instruction(question_schema=question_schema)
        self.answer_description = self._build_answer_descriptions(
            answers=iter(question_schema["answers"])
        )
        self.answer_guidance = self._build_answer_guidance(
            answers=iter(question_schema["answers"])
        )

    def _build_answers(
        self,
    ):
        answers = []
        for answer in self.answer_schemas:
            if options := answer.get("options"):
                for option in options:
                    answers.append(option["label"])
            if not options:
                answers.append(answer["label"])

        return answers

    def _build_answer_descriptions(self, *, answers):
        for answer in answers:
            if answer.get("description"):
                return answer.get("description")
        return None

    def _build_answer_guidance(self, *, answers):
        for answer in answers:
            if guidance := answer.get("guidance"):
                return guidance.get("show_guidance")
        return None

    def _build_descriptions(
        self,
        *,
        question_schema,
    ):
        if description := question_schema.get("description"):

            return description

        return None

    def _build_guidance(
        self,
        *,
        question_schema,
    ):
        if guidance := question_schema.get("guidance"):
            guidance_list = []
            for contents in guidance.get("contents"):
                if contents.get("description"):
                    guidance_list.append(contents.get("description"))
                elif contents.get("list"):
                    guidance_items = []
                    for item in contents.get("list"):
                        guidance_items.append(item)
                    guidance_list.append(guidance_items)
            return guidance_list

        return None

    def _get_length(
        self,
        *,
        question_schema,
    ):
        if answers := question_schema.get("answers"):
            for answer in answers:
                if answer.get("type") == "TextArea":
                    return answer.get("max_length")

        return None

    def _build_instruction(
        self,
        *,
        question_schema,
    ):
        if instruction := question_schema.get("instruction"):
            return instruction
        return None

    def serialize(self):
        return {
            "id": self.id,
            "type": self.type,
            "title": self.title,
            "number": self.number,
            "answers": self.answers,
            "descriptions": self.descriptions,
            "guidance": self.guidance,
            "text_length": self.text_length,
            "instruction": self.instruction,
            "answer_description": self.answer_description,
            "answer_guidance": self.answer_guidance,
        }
