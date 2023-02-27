from typing import Any, Union

from werkzeug.datastructures import ImmutableDict


class PreviewQuestion:
    def __init__(
        self,
        *,
        block: ImmutableDict,
    ):
        self._block = block
        self._block_id = block["id"]
        self._question = self.get_question()
        self._title = self._question["title"]
        self._answers = self._build_answers()
        self._descriptions = self._question.get("description")
        self._guidance = self._question.get("guidance")
        self._instruction = self._question.get("instruction")
        self._type = self._question.get("type")

    def _build_answers(self) -> list[dict]:
        answers_list = []
        for answer in self._question.get("answers", []):
            answer_dict = {}
            if answer_label := answer.get("label"):
                answer_dict["label"] = answer_label

            if options := answer.get("options"):
                options_list = [option["label"] for option in options]
                answer_dict["options"] = options_list

            if description := answer.get("description"):
                answer_dict["description"] = description

            if instruction := answer.get("instruction"):
                answer_dict["instruction"] = instruction

            if guidance := answer.get("guidance"):
                answer_dict["guidance"] = guidance

            if answer.get("type") == "TextArea" and (
                length := answer.get("max_length")
            ):
                answer_dict["max_length"] = length

            answers_list.append(answer_dict)
        return answers_list

    def serialize(self) -> dict[str, Union[str, dict, Any]]:
        return {
            "id": self._block_id,
            "title": self._title,
            "answers": self._answers,
            "descriptions": self._descriptions,
            "guidance": self._guidance,
            "instruction": self._instruction,
            "type": self._type,
        }

    def get_question(self) -> Any:
        if "question_variants" in self._block:
            return self._block["question_variants"][0]["question"]

        return self._block["question"]
