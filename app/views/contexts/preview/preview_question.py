from typing import Any, Optional, Union

from app.data_models import QuestionnaireStore
from app.questionnaire import Location, QuestionnaireSchema, QuestionSchemaType
from app.questionnaire.placeholder_renderer import PlaceholderRenderer
from app.questionnaire.variants import transform_variants


class PreviewQuestion:
    def __init__(
        self,
        schema: QuestionnaireSchema,
        questionnaire_store: QuestionnaireStore,
        section_id: str,
        block_id: str,
        language: str,
    ):
        self.schema = schema
        self.questionnaire_store = questionnaire_store
        self.current_location = Location(section_id=section_id, block_id=block_id)
        self.block_id = block_id

        self.placeholder_renderer = PlaceholderRenderer(
            language=language,
            answer_store=self.questionnaire_store.answer_store,
            list_store=self.questionnaire_store.list_store,
            metadata=self.questionnaire_store.metadata,
            response_metadata=self.questionnaire_store.response_metadata,
            schema=self.schema,
            location=self.current_location,
            preview_mode=True,
        )

        self.question = self.rendered_block().get("question")

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
            for answer in iter(answers):
                if options := answer.get("options"):
                    labels.extend(option["label"] for option in options)
                if not options:
                    labels.append(answer["label"])

        return labels

    def _build_answer_descriptions(self) -> Optional[dict]:
        answers = iter(self.question["answers"])  # type: ignore
        return next(
            (
                answer.get("description")
                for answer in answers
                if answer.get("description")
            ),
            None,
        )

    def _build_answer_guidance(self) -> Optional[list[Any]]:
        answers = iter(self.question["answers"])  # type: ignore
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

    def rendered_block(self) -> dict[str, Any]:
        transformed_block = transform_variants(
            self.schema.get_block(self.current_location.block_id),  # type: ignore
            self.schema,
            self.questionnaire_store.metadata,
            self.questionnaire_store.response_metadata,
            self.questionnaire_store.answer_store,
            self.questionnaire_store.list_store,
            self.current_location,
        )

        return self.placeholder_renderer.render(transformed_block, None)
