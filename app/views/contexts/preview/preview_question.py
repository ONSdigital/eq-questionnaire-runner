from typing import Any, Optional, Union

from werkzeug.datastructures import ImmutableDict

from app.questionnaire import QuestionnaireSchema, QuestionSchemaType


class PreviewQuestion:
    def __init__(
        self,
        *,
        block: ImmutableDict,
    ):
        self.block = block
        self.block_id = block.get("id")
        self.question = self.resolved_block().get("question")
        # render_block returns same type as placeholder_renderer.render which is dict[str, Any] hence all type ignores below

        self.title = self.question.get("title")  # type: ignore

        self.answers = self._build_answers()
        self.descriptions = self._build_descriptions()
        self.guidance = self._build_question_guidance()
        self.text_length = self._get_length()
        self.instruction = self.question.get("instruction")  # type: ignore
        self.answer_description = self._build_answer_descriptions()
        self.answer_guidance = self._build_answer_guidance()

    def _build_answers(self) -> list[Optional[str]]:
        labels: list = []
        if answers := self.question.get("answers"):  # type: ignore
            for answer in answers:
                if options := answer.get("options"):
                    labels.extend(option["label"] for option in options)
                if not options:
                    labels.append(answer["label"])

        return labels

    def _build_answer_descriptions(self) -> Optional[dict]:
        answers = self.question["answers"]  # type: ignore
        return next(
            (
                answer.get("description")
                for answer in answers
                if answer.get("description")
            ),
            None,
        )

    def _build_answer_guidance(self) -> Optional[list[Any]]:
        answers = self.question["answers"]  # type: ignore
        for answer in answers:
            return self._build_guidance(answer)

    def _build_descriptions(self) -> Any:
        return descriptions if (descriptions := self.question.get("description")) else None  # type: ignore

    def _build_question_guidance(self) -> Optional[list[Any]]:
        return self._build_guidance(self.question)  # type: ignore

    @staticmethod
    def _build_guidance(schema_element: QuestionSchemaType) -> Optional[list[dict]]:
        return guidance if (guidance := schema_element.get("guidance")) else None

    def _get_length(self) -> Optional[Any]:
        answers = self.question.get("answers")  # type: ignore
        return next(
            (
                answer.get("max_length")
                for answer in answers
                if answer.get("type") == "TextArea"
            ),
            None,
        )

    def serialize(self) -> dict[str, Union[str, dict, Any]]:
        return {
            "id": self.block_id,
            "title": self.title,
            "answers": self.answers,
            "descriptions": self.descriptions,
            "guidance": self.guidance,
            "text_length": self.text_length,
            "instruction": self.instruction,
            "answer_description": self.answer_description,
            "answer_guidance": self.answer_guidance,
        }

    def resolved_block(self) -> dict[str, Any]:
        output_block: dict = QuestionnaireSchema.get_mutable_deepcopy(self.block)
        if "question_variants" in self.block:
            output_block.pop("question_variants", None)
            output_block.pop("question", None)

            output_block["question"] = QuestionnaireSchema.get_mutable_deepcopy(
                self.block["question_variants"][0]["question"]
            )
        return output_block
