from typing import Any

from flask_babel import lazy_gettext
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
        self._type = self._question.get("type")

    def _build_answers(self) -> list[dict]:
        answers_list = []
        for answer in self._question.get("answers", []):
            answer_dict = {}
            answer_type = answer.get("type")
            if options := answer.get("options"):
                options_list = [option["label"] for option in options]
                answer_dict["options"] = options_list
                if answer_type == "Checkbox":
                    answer_dict["options_text"] = lazy_gettext(
                        "You can answer with the following options:"
                    )
                else:
                    answer_dict["options_text"] = lazy_gettext(
                        "You can answer with one of the following options:"
                    )
            elif answer_label := answer.get("label"):
                answer_dict["label"] = answer_label

            if description := answer.get("description"):
                answer_dict["description"] = description

            if guidance := answer.get("guidance"):
                answer_dict["guidance"] = guidance

            if answer_type == "TextArea" and (length := answer.get("max_length")):
                answer_dict["max_length"] = length

            answers_list.append(answer_dict)
        return answers_list

    def serialize(self) -> dict[str, str | dict | Any]:
        return {
            "id": self._block_id,
            "title": self._title,
            "answers": self._answers,
            "descriptions": self._descriptions,
            "guidance": self._guidance,
            "type": self._type,
        }

    def get_question(self) -> Any:
        if "question_variants" in self._block:
            return self._block["question_variants"][0]["question"]

        return self._block["question"]
