from typing import Any, Union

from werkzeug.datastructures import ImmutableDict

from app.questionnaire import QuestionnaireSchema


class PreviewQuestion:
    def __init__(
        self,
        *,
        block: ImmutableDict,
    ):
        self._block = block
        self._block_id = block.get("id")
        self._question = self.resolve_variants().get("question")
        # resolve_variants returns same type as placeholder_renderer.render which is dict[str, Any] hence all type ignores below
        self._title = self._question.get("title")  # type: ignore
        self._answers = self._build_answers()
        self._descriptions = self._question.get("description")  # type: ignore
        self._guidance = self._question.get("guidance")  # type: ignore
        self._instruction = self._question.get("instruction")  # type: ignore

    def _build_answers(self) -> list[dict]:
        answers_list = []
        if answers := self._question.get("answers"):  # type: ignore
            for answer in answers:
                if options := answer.get("options"):
                    options_list = [option["label"] for option in options]
                    answer_dict = {"options": options_list}
                else:
                    answer_dict = {"label": answer["label"]}
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
        }

    def resolve_variants(self) -> dict[str, Any]:
        output_block: dict = QuestionnaireSchema.get_mutable_deepcopy(self._block)
        if "question_variants" in self._block:
            output_block.pop("question_variants", None)
            output_block.pop("question", None)

            output_block["question"] = QuestionnaireSchema.get_mutable_deepcopy(
                self._block["question_variants"][0]["question"]
            )
        return output_block
