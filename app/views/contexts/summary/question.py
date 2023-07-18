from typing import Any, Mapping, MutableMapping, Optional

from flask import url_for
from markupsafe import Markup, escape
from werkzeug.datastructures import ImmutableDict

from app.data_models import (
    AnswerStore,
    ListStore,
    ProgressStore,
    SupplementaryDataStore,
)
from app.data_models.answer import AnswerValueEscapedTypes, escape_answer_value
from app.data_models.metadata_proxy import MetadataProxy
from app.forms.field_handlers.select_handlers import DynamicAnswerOptions
from app.questionnaire import Location, QuestionnaireSchema, QuestionSchemaType
from app.questionnaire.placeholder_renderer import PlaceholderRenderer
from app.questionnaire.rules.rule_evaluator import RuleEvaluator
from app.questionnaire.value_source_resolver import ValueSourceResolver
from app.views.contexts.summary.answer import (
    Answer,
    InferredAnswerValueTypes,
    RadioCheckboxTypes,
)


# pylint: disable=too-many-locals
class Question:
    def __init__(
        self,
        question_schema: QuestionSchemaType,
        *,
        answer_store: AnswerStore,
        list_store: ListStore,
        progress_store: ProgressStore,
        supplementary_data_store: SupplementaryDataStore,
        schema: QuestionnaireSchema,
        rule_evaluator: RuleEvaluator,
        value_source_resolver: ValueSourceResolver,
        location: Location,
        block_id: str,
        return_to: Optional[str],
        return_to_block_id: Optional[str] = None,
        metadata: MetadataProxy | None,
        response_metadata: MutableMapping,
        language: str,
    ) -> None:
        self.list_item_id = location.list_item_id if location else None
        self.id = question_schema["id"]
        self.type = question_schema["type"]
        self.schema = schema
        self.answer_schemas = iter(question_schema.get("answers", []))
        self.answer_store = answer_store
        self.list_store = list_store
        self.progress_store = progress_store
        self.supplementary_data_store = supplementary_data_store
        self.summary = question_schema.get("summary")
        self.title = (
            question_schema.get("title") or question_schema["answers"][0]["label"]
        )
        self.number = question_schema.get("number", None)

        self.rule_evaluator = rule_evaluator
        self.value_source_resolver = value_source_resolver
        # no need to call the method if no list item id
        self._is_in_repeating_section = bool(
            self.list_item_id and self.schema.is_block_in_repeating_section(block_id)
        )

        self.answers = self._build_answers(
            answer_store=answer_store,
            question_schema=question_schema,
            block_id=block_id,
            list_name=location.list_name if location else None,
            return_to=return_to,
            return_to_block_id=return_to_block_id,
            metadata=metadata,
            response_metadata=response_metadata,
            language=language,
        )

    def get_answer(
        self, answer_store: AnswerStore, answer_id: str, list_item_id: str | None = None
    ) -> Optional[AnswerValueEscapedTypes]:
        answer = answer_store.get_answer(
            answer_id, list_item_id or self.list_item_id
        ) or self.schema.get_default_answer(answer_id)

        return escape_answer_value(answer.value) if answer else None

    def _build_answers(
        self,
        *,
        answer_store: AnswerStore,
        question_schema: QuestionSchemaType,
        block_id: str,
        list_name: str | None,
        return_to: str | None,
        return_to_block_id: str | None,
        metadata: MetadataProxy | None,
        response_metadata: MutableMapping,
        language: str,
    ) -> list[dict[str, Any]]:
        if self.summary:
            answer_id = f"{self.id}-concatenated-answer"
            link = url_for(
                "questionnaire.block",
                list_name=list_name,
                block_id=block_id,
                list_item_id=self.list_item_id,
                return_to=return_to,
                return_to_answer_id=answer_id if return_to else None,
                _anchor=question_schema["answers"][0]["id"],
            )

            return [
                {
                    "id": answer_id,
                    "value": self._concatenate_answers(
                        answer_store, self.summary["concatenation_type"]
                    ),
                    "link": link,
                }
            ]

        summary_answers = []

        for answer_schema in self._get_resolved_answers(
            question_schema=question_schema,
            language=language,
            metadata=metadata,
            response_metadata=response_metadata,
        ):
            list_item_id = answer_schema.get("list_item_id")
            answer_id = answer_schema.get("original_answer_id") or answer_schema["id"]
            answer_value = self.get_answer(
                answer_store, answer_id, list_item_id=list_item_id
            )
            answer = self._build_answer(
                answer_store, question_schema, answer_schema, answer_value
            )

            summary_answer = Answer(
                answer_schema=answer_schema,
                answer_value=answer,
                block_id=block_id,
                list_name=list_name,
                list_item_id=list_item_id or self.list_item_id,
                return_to=return_to,
                return_to_block_id=return_to_block_id,
                is_in_repeating_section=self._is_in_repeating_section,
            ).serialize()
            summary_answers.append(summary_answer)

        if question_schema["type"] == "MutuallyExclusive":
            exclusive_option = summary_answers[-1]["value"]
            if exclusive_option:
                return summary_answers[-1:]
            return summary_answers[:-1]
        return summary_answers

    def _concatenate_answers(
        self, answer_store: AnswerStore, concatenation_type: str
    ) -> str:
        answer_separators = {"Newline": "<br>", "Space": " "}
        answer_separator = answer_separators.get(concatenation_type, " ")

        answer_values = [
            self.get_answer(answer_store, answer_schema["id"])
            for answer_schema in self.answer_schemas
        ]

        values_to_concatenate: list[AnswerValueEscapedTypes] = []
        for answer_value in answer_values:
            if not answer_value:
                continue

            if isinstance(answer_value, list):
                values_to_concatenate.extend(answer_value)
            else:
                values_to_concatenate.append(answer_value)

        return answer_separator.join(str(value) for value in values_to_concatenate)

    def _build_answer(
        self,
        answer_store: AnswerStore,
        question_schema: QuestionSchemaType,
        answer_schema: Mapping[str, Any],
        answer_value: Optional[AnswerValueEscapedTypes] = None,
    ) -> InferredAnswerValueTypes:
        if answer_value is None:
            return None

        if question_schema["type"] == "DateRange":
            return self._build_date_range_answer(answer_store, answer_value)

        if answer_schema["type"] == "Dropdown":
            return self._build_dropdown_answer(answer_value, answer_schema)

        answer_builder = {
            "Checkbox": self._build_checkbox_answers,
            "Radio": self._build_radio_answer,
        }
        # Type ignore: Answer value will be a Markup(String) at this stage
        if answer_schema["type"] in answer_builder:
            return answer_builder[answer_schema["type"]](answer_value, answer_schema, answer_store)  # type: ignore

        return answer_value

    def _build_date_range_answer(
        self, answer_store: AnswerStore, answer: Optional[AnswerValueEscapedTypes]
    ) -> dict[str, Optional[AnswerValueEscapedTypes]]:
        next_answer = next(self.answer_schemas)
        to_date = self.get_answer(answer_store, next_answer["id"])
        return {"from": answer, "to": to_date}

    def _get_dynamic_answer_options(
        self,
        answer_schema: Mapping[str, Any],
    ) -> tuple[dict[str, str], ...]:
        if not (dynamic_options_schema := answer_schema.get("dynamic_options")):
            return ()

        dynamic_options = DynamicAnswerOptions(
            dynamic_options_schema=dynamic_options_schema,
            rule_evaluator=self.rule_evaluator,
            value_source_resolver=self.value_source_resolver,
        )

        return dynamic_options.evaluate()

    def get_answer_options(
        self, answer_schema: Mapping[str, Any]
    ) -> tuple[dict[str, str], ...]:
        return tuple(answer_schema.get("options", ())) + tuple(
            self._get_dynamic_answer_options(answer_schema)
        )

    def _build_checkbox_answers(
        self,
        answer: Markup,
        answer_schema: Mapping[str, Any],
        answer_store: AnswerStore,
    ) -> Optional[list[RadioCheckboxTypes]]:
        multiple_answers = []
        for option in self.get_answer_options(answer_schema):
            if escape(option["value"]) in answer:
                detail_answer_value = self._get_detail_answer_value(
                    option, answer_store
                )

                multiple_answers.append(
                    {
                        "label": option["label"],
                        "detail_answer_value": detail_answer_value,
                    }
                )

        return multiple_answers or None

    def _build_radio_answer(
        self,
        answer: Markup,
        answer_schema: Mapping[str, Any],
        answer_store: AnswerStore,
    ) -> Optional[RadioCheckboxTypes]:
        for option in self.get_answer_options(answer_schema):
            if answer == escape(option["value"]):
                detail_answer_value = self._get_detail_answer_value(
                    option, answer_store
                )
                return {
                    "label": option["label"],
                    "detail_answer_value": detail_answer_value,
                }

    def _get_detail_answer_value(
        self, option: dict, answer_store: AnswerStore
    ) -> Optional[AnswerValueEscapedTypes]:
        if "detail_answer" in option:
            return self.get_answer(answer_store, option["detail_answer"]["id"])

    def _build_dropdown_answer(
        self,
        answer: Optional[AnswerValueEscapedTypes],
        answer_schema: Mapping[str, Any],
    ) -> Optional[str]:
        for option in self.get_answer_options(answer_schema):
            if answer == option["value"]:
                return option["label"]

    def _get_resolved_answers(
        self,
        *,
        question_schema: QuestionSchemaType,
        language: str,
        metadata: MetadataProxy | None = None,
        response_metadata: MutableMapping,
    ) -> Any:
        resolved_question = ImmutableDict({"answers": self.answer_schemas})

        if "dynamic_answers" in question_schema:
            placeholder_renderer = PlaceholderRenderer(
                answer_store=self.answer_store,
                list_store=self.list_store,
                progress_store=self.progress_store,
                schema=self.schema,
                language=language,
                metadata=metadata,
                response_metadata=response_metadata,
                supplementary_data_store=self.supplementary_data_store,
            )

            resolved_question = ImmutableDict(
                placeholder_renderer.render(
                    data_to_render=question_schema, list_item_id=self.list_item_id
                )
            )
        return resolved_question["answers"]

    def serialize(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type,
            "title": self.title,
            "number": self.number,
            "answers": self.answers,
        }
