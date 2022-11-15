from typing import Any, Mapping, MutableMapping, Optional, Union

from jsonpointer import resolve_pointer, set_pointer

from app.data_models.answer import AnswerValueTypes
from app.data_models.answer_store import AnswerStore
from app.data_models.list_store import ListStore
from app.data_models.metadata_proxy import MetadataProxy
from app.questionnaire import Location, QuestionnaireSchema
from app.questionnaire.placeholder_parser import PlaceholderParser
from app.questionnaire.plural_forms import get_plural_form_key
from app.questionnaire.relationship_location import RelationshipLocation
from app.questionnaire.schema_utils import find_pointers_containing


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
        metadata: Optional[MetadataProxy],
        response_metadata: Mapping,
        schema: QuestionnaireSchema,
        location: Union[None, Location, RelationshipLocation] = None,
    ):
        self._language = language
        self._answer_store = answer_store
        self._list_store = list_store
        self._metadata = metadata
        self._response_metadata = response_metadata
        self._schema = schema
        self._location = location

    def render_pointer(
        self,
        dict_to_render: Mapping[str, Any],
        pointer_to_render: str,
        list_item_id: Optional[str],
    ) -> str:
        pointer_data = resolve_pointer(dict_to_render, pointer_to_render)

        return self.render_placeholder(pointer_data, list_item_id)

    def get_plural_count(
        self, schema_partial: Mapping[str, str]
    ) -> Optional[AnswerValueTypes]:
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
        placeholder_data: MutableMapping[str, Any],
        list_item_id: Optional[str],
    ) -> str:
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
        )

        placeholder_data = QuestionnaireSchema.get_mutable_deepcopy(placeholder_data)

        if "text_plural" in placeholder_data:
            plural_schema: Mapping[str, dict] = placeholder_data["text_plural"]
            count = self.get_plural_count(plural_schema["count"])

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
        self, dict_to_render: Mapping[str, Any], list_item_id: Optional[str]
    ) -> Mapping[str, Any]:
        """
        Transform the current schema json to a fully rendered dictionary
        """
        dict_to_render = QuestionnaireSchema.get_mutable_deepcopy(dict_to_render)
        pointers = find_pointers_containing(dict_to_render, "placeholders")

        for pointer in pointers:
            rendered_text = self.render_pointer(dict_to_render, pointer, list_item_id)
            set_pointer(dict_to_render, pointer, rendered_text)

        return dict_to_render
