from jsonpointer import resolve_pointer, set_pointer

from app.data_models.answer_store import AnswerStore
from app.questionnaire import QuestionnaireSchema
from app.questionnaire.placeholder_parser import PlaceholderParser
from app.questionnaire.plural_forms import get_plural_form_key
from app.questionnaire.schema_utils import find_pointers_containing


class PlaceholderRenderer:
    """
    Renders placeholders specified by a list of pointers in a schema block to their final
    strings
    """

    def __init__(
        self,
        language,
        schema,
        answer_store=None,
        list_store=None,
        metadata=None,
        location=None,
    ):
        self._language = language
        self._schema = schema
        self._answer_store = answer_store or AnswerStore()
        self._list_store = list_store
        self._metadata = metadata
        self._location = location

    def render_pointer(self, dict_to_render, pointer_to_render, list_item_id):
        pointer_data = resolve_pointer(dict_to_render, pointer_to_render)

        return self.render_placeholder(pointer_data, list_item_id)

    def get_plural_count(self, schema_partial):
        source = schema_partial["source"]
        source_id = schema_partial["identifier"]

        if source == "answers":
            return self._answer_store.get_answer(source_id).value
        if source == "list":
            return len(self._list_store[source_id])
        return self._metadata[source_id]

    def render_placeholder(self, placeholder_data, list_item_id):
        placeholder_parser = PlaceholderParser(
            language=self._language,
            schema=self._schema,
            answer_store=self._answer_store,
            metadata=self._metadata,
            list_item_id=list_item_id,
            location=self._location,
            list_store=self._list_store,
        )

        placeholder_data = QuestionnaireSchema.get_mutable_deepcopy(placeholder_data)

        if "text_plural" in placeholder_data:
            plural_schema = placeholder_data["text_plural"]
            count = self.get_plural_count(plural_schema["count"])

            plural_form_key = get_plural_form_key(count, self._language)
            placeholder_data["text"] = plural_schema["forms"][plural_form_key]

        if "text" not in placeholder_data and "placeholders" not in placeholder_data:
            raise ValueError("No placeholder found to render")

        transformed_values = placeholder_parser(placeholder_data["placeholders"])

        return placeholder_data["text"].format(**transformed_values)

    def render(self, dict_to_render, list_item_id):
        """
        Transform the current schema json to a fully rendered dictionary
        """
        dict_to_render = QuestionnaireSchema.get_mutable_deepcopy(dict_to_render)
        pointers = find_pointers_containing(dict_to_render, "placeholders")

        for pointer in pointers:
            rendered_text = self.render_pointer(dict_to_render, pointer, list_item_id)
            set_pointer(dict_to_render, pointer, rendered_text)

        return dict_to_render
