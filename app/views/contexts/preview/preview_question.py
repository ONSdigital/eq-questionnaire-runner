from typing import Any, Mapping, Optional, Union

from app.data_models import AnswerStore, ListStore
from app.data_models.metadata_proxy import MetadataProxy
from app.questionnaire import Location, QuestionnaireSchema, QuestionSchemaType
from app.questionnaire.placeholder_renderer import PlaceholderRenderer


class PreviewQuestion:
    def __init__(
        self,
        *,
        schema: QuestionnaireSchema,
        answer_store: AnswerStore,
        list_store: ListStore,
        metadata: Optional[MetadataProxy],
        response_metadata: Mapping[str, Union[str, int, list]],
        section_id: str,
        block_id: str,
        language: str,
    ):
        self.schema = schema
        self.answer_store = answer_store
        self.list_store = list_store
        self.metadata = metadata
        self.response_metadata = response_metadata
        self.current_location = Location(section_id=section_id, block_id=block_id)
        self.block_id = block_id

        self.placeholder_renderer = PlaceholderRenderer(
            language=language,
            answer_store=self.answer_store,
            list_store=self.list_store,
            metadata=self.metadata,
            response_metadata=self.response_metadata,
            schema=self.schema,
            location=self.current_location,
            preview_mode=True,
        )

        self.question = self.rendered_block().get("question")
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

    def rendered_block(self) -> dict[str, Any]:
        block = self.schema.get_block(self.current_location.block_id)  # type: ignore
        # block exists at this point, get_block() returns Optional
        output_block = self.schema.get_mutable_deepcopy(block)  # type: ignore
        # method returns Any
        if "question_variants" in block:  # type: ignore
            # Optional dict as return of get_block()
            output_block.pop("question_variants", None)
            output_block.pop("question", None)

            output_block["question"] = self.schema.get_mutable_deepcopy(block["question_variants"][0]["question"])  # type: ignore
            # Same as above
        return self.placeholder_renderer.render(output_block, None)
