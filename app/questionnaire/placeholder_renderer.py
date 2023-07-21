from copy import deepcopy
from typing import Any, Mapping, MutableMapping

from jsonpointer import resolve_pointer, set_pointer

from app.data_models import ProgressStore
from app.data_models.answer import AnswerValueTypes
from app.data_models.answer_store import AnswerStore
from app.data_models.list_store import ListStore
from app.data_models.metadata_proxy import MetadataProxy
from app.questionnaire import QuestionnaireSchema
from app.questionnaire.placeholder_parser import PlaceholderParser
from app.questionnaire.plural_forms import get_plural_form_key
from app.questionnaire.schema_utils import find_pointers_containing
from app.utilities.types import LocationType


class PlaceholderRenderer:
    """
    Renders placeholders specified by a list of pointers in a schema block to their final
    strings
    """

    def __init__(
        self,
        language: str,
        answer_store: AnswerStore,
        list_store: ListStore,
        metadata: MetadataProxy | None,
        response_metadata: MutableMapping,
        schema: QuestionnaireSchema,
        progress_store: ProgressStore,
        location: LocationType | None = None,
        placeholder_preview_mode: bool | None = False,
    ):
        self._placeholder_preview_mode = placeholder_preview_mode
        self._language = language
        self._answer_store = answer_store
        self._list_store = list_store
        self._metadata = metadata
        self._response_metadata = response_metadata
        self._schema = schema
        self._location = location
        self._progress_store = progress_store

    def render_pointer(
        self,
        *,
        dict_to_render: Mapping,
        pointer_to_render: str,
        list_item_id: str | None,
        placeholder_parser: PlaceholderParser,
    ) -> str:
        pointer_data = resolve_pointer(dict_to_render, pointer_to_render)

        return self.render_placeholder(pointer_data, list_item_id, placeholder_parser)

    def get_plural_count(
        self, schema_partial: Mapping[str, str]
    ) -> AnswerValueTypes | None:
        source = schema_partial["source"]
        source_id = schema_partial["identifier"]

        if source == "answers":
            answer = self._answer_store.get_answer(source_id)
            return answer.value if answer else None
        if source == "list":
            return len(self._list_store[source_id])

        return self._metadata[source_id] if self._metadata else None

    def render_placeholder(
        self,
        placeholder_data: MutableMapping,
        list_item_id: str | None,
        placeholder_parser: PlaceholderParser | None = None,
    ) -> str:
        if not placeholder_parser:
            placeholder_parser = PlaceholderParser(
                language=self._language,
                answer_store=self._answer_store,
                list_store=self._list_store,
                metadata=self._metadata,
                response_metadata=self._response_metadata,
                schema=self._schema,
                list_item_id=list_item_id,
                location=self._location,
                renderer=self,
                progress_store=self._progress_store,
                placeholder_preview_mode=self._placeholder_preview_mode,
            )

        placeholder_data = QuestionnaireSchema.get_mutable_deepcopy(placeholder_data)

        if "text_plural" in placeholder_data:
            plural_schema: Mapping[str, dict] = placeholder_data["text_plural"]
            # Type ignore: For a valid schema the plural count will return an integer
            count: int = (
                0  # type: ignore
                if self._placeholder_preview_mode
                else self.get_plural_count(plural_schema["count"])
            )

            plural_form_key = get_plural_form_key(count, self._language)
            plural_forms: Mapping[str, str] = plural_schema["forms"]
            placeholder_data["text"] = plural_forms[plural_form_key]

        if "text" not in placeholder_data and "placeholders" not in placeholder_data:
            raise ValueError("No placeholder found to render")

        transformed_values = placeholder_parser(placeholder_data["placeholders"])
        formatted_placeholder_data: str = placeholder_data["text"].format(
            **transformed_values
        )

        return formatted_placeholder_data

    def render(
        self,
        *,
        data_to_render: Mapping,
        list_item_id: str | None,
    ) -> dict:
        """
        Transform the current schema json to a fully rendered dictionary
        """
        data_to_render_mutable: dict[
            str, Any
        ] = QuestionnaireSchema.get_mutable_deepcopy(data_to_render)

        self._handle_and_resolve_dynamic_answers(data_to_render_mutable)

        pointers = find_pointers_containing(data_to_render_mutable, "placeholders")

        placeholder_parser = PlaceholderParser(
            language=self._language,
            answer_store=self._answer_store,
            list_store=self._list_store,
            metadata=self._metadata,
            response_metadata=self._response_metadata,
            schema=self._schema,
            list_item_id=list_item_id,
            location=self._location,
            renderer=self,
            placeholder_preview_mode=self._placeholder_preview_mode,
            progress_store=self._progress_store,
        )

        for pointer in pointers:
            rendered_text = self.render_pointer(
                dict_to_render=data_to_render_mutable,
                pointer_to_render=pointer,
                list_item_id=list_item_id,
                placeholder_parser=placeholder_parser,
            )
            set_pointer(data_to_render_mutable, pointer, rendered_text)
        return data_to_render_mutable

    def _handle_and_resolve_dynamic_answers(
        self, data_to_render_mutable: dict[str, Any]
    ) -> None:
        pointers = find_pointers_containing(data_to_render_mutable, "dynamic_answers")

        for pointer in pointers:
            data = resolve_pointer(data_to_render_mutable, pointer)
            dynamic_answers = data["dynamic_answers"]

            if dynamic_answers["values"]["source"] == "list":
                self.resolve_dynamic_answers_ids(dynamic_answers)
                self.resolve_dynamic_answers(dynamic_answers)

                updated_value = {
                    "answers": dynamic_answers["answers"] + data.get("answers", []),
                    "dynamic_answers": dynamic_answers,
                }

                del updated_value["dynamic_answers"]["answers"]

                if pointer:
                    set_pointer(data_to_render_mutable, pointer, updated_value)
                else:
                    data_to_render_mutable |= updated_value

    def resolve_dynamic_answers_ids(
        self,
        dynamic_answers: dict,
    ) -> None:
        list_name = dynamic_answers["values"]["identifier"]
        list_items = self._list_store[list_name].items

        resolved_dynamic_answers = []

        for dynamic_answer in dynamic_answers["answers"]:
            for item in list_items:
                resolved_dynamic_answer = deepcopy(dynamic_answer)
                resolved_dynamic_answer["original_answer_id"] = dynamic_answer["id"]
                resolved_dynamic_answer["id"] = f"{dynamic_answer['id']}-{item}"
                resolved_dynamic_answer["list_item_id"] = item

                resolved_dynamic_answers.append(resolved_dynamic_answer)

        dynamic_answers["answers"] = resolved_dynamic_answers

    def resolve_dynamic_answers(
        self,
        dynamic_answers: dict,
    ) -> None:
        for answer in dynamic_answers["answers"]:
            placeholder_parser = PlaceholderParser(
                language=self._language,
                answer_store=self._answer_store,
                list_store=self._list_store,
                metadata=self._metadata,
                response_metadata=self._response_metadata,
                schema=self._schema,
                list_item_id=answer["list_item_id"],
                location=self._location,
                renderer=self,
                placeholder_preview_mode=self._placeholder_preview_mode,
                progress_store=self._progress_store,
            )

            pointers = find_pointers_containing(answer, "placeholders")

            for pointer in pointers:
                rendered_text = self.render_pointer(
                    dict_to_render=answer,
                    pointer_to_render=pointer,
                    list_item_id=answer["list_item_id"],
                    placeholder_parser=placeholder_parser,
                )
                set_pointer(answer, pointer, rendered_text)
