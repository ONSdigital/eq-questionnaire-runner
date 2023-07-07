from typing import Any, Iterable, Mapping, MutableMapping, Sequence

from werkzeug.datastructures import ImmutableDict

from app.data_models import AnswerStore, ProgressStore
from app.data_models.list_store import ListModel, ListStore
from app.data_models.metadata_proxy import MetadataProxy
from app.questionnaire import Location, QuestionnaireSchema
from app.questionnaire.placeholder_renderer import PlaceholderRenderer
from app.views.contexts import list_context
from app.views.contexts.summary.block import Block


class ListCollectorContentBlock:
    def __init__(
        self,
        routing_path_block_ids: Iterable[str],
        answer_store: AnswerStore,
        list_store: ListStore,
        progress_store: ProgressStore,
        metadata: MetadataProxy | None,
        response_metadata: MutableMapping,
        schema: QuestionnaireSchema,
        location: Location,
        language: str,
    ) -> None:
        self._location = location
        self._placeholder_renderer = PlaceholderRenderer(
            language=language,
            answer_store=answer_store,
            list_store=list_store,
            metadata=metadata,
            response_metadata=response_metadata,
            schema=schema,
            progress_store=progress_store,
            location=location,
        )
        self._list_store = list_store
        self._schema = schema
        self._location = location
        # type ignore added as section should exist
        self._section: ImmutableDict = self._schema.get_section(self._location.section_id)  # type: ignore
        self._language = language
        self._answer_store = answer_store
        self._metadata = metadata
        self._response_metadata = response_metadata
        self._routing_path_block_ids = routing_path_block_ids
        self._progress_store = progress_store

    # pylint: disable=too-many-locals
    def list_summary_element(self, summary: Mapping[str, Any]) -> dict[str, Any]:
        related_answers = None

        current_list = self._list_store[summary["for_list"]]

        list_collector_blocks = list(
            self._schema.get_list_collectors_for_list(
                self._section, for_list=summary["for_list"]
            )
        )

        list_collector_blocks_on_path = [
            list_collector_block
            for list_collector_block in list_collector_blocks
            if list_collector_block["id"] in self._routing_path_block_ids
        ]

        list_collector_block = (
            list_collector_blocks_on_path[0]
            if list_collector_blocks_on_path
            else list_collector_blocks[0]
        )

        rendered_summary = self._placeholder_renderer.render(
            data_to_render=summary, list_item_id=self._location.list_item_id
        )

        if list_collector_blocks_on_path:
            repeating_blocks = list_collector_block.get("repeating_blocks", [])
            related_answers = self._get_related_answers(current_list, repeating_blocks)

        list_summary_context = self.list_context(
            list_collector_block["summary"],
            for_list=list_collector_block["for_list"],
            section_id=self._location.section_id,
            has_repeating_blocks=bool(list_collector_block.get("repeating_blocks")),
            return_to="section-summary",
            content_definition=ImmutableDict({}),
        )

        return {
            "title": rendered_summary["title"],
            "type": rendered_summary["type"],
            "empty_list_text": None,
            "list_name": rendered_summary["for_list"],
            "related_answers": related_answers,
            **list_summary_context,
        }

    @property
    def list_context(self) -> list_context.ListContext:
        return list_context.ListContext(
            self._language,
            self._schema,
            self._answer_store,
            self._list_store,
            self._progress_store,
            self._metadata,
            self._response_metadata,
        )

    def _get_related_answers(
        self, list_model: ListModel, repeating_blocks: Sequence[ImmutableDict]
    ) -> dict[str, list[dict]] | None:
        section_id = self._section["id"]

        blocks: list[dict | ImmutableDict] = []

        if len(list_model):
            blocks += repeating_blocks

        related_answers_blocks = {}

        for list_id in list_model:
            serialized_blocks = [
                Block(
                    block,
                    answer_store=self._answer_store,
                    list_store=self._list_store,
                    metadata=self._metadata,
                    response_metadata=self._response_metadata,
                    schema=self._schema,
                    location=Location(
                        list_name=list_model.name,
                        list_item_id=list_id,
                        section_id=section_id,
                    ),
                    return_to="section-summary",
                    return_to_block_id=None,
                    progress_store=self._progress_store,
                    language=self._language,
                ).serialize()
                for block in blocks
            ]

            related_answers_blocks[list_id] = serialized_blocks

        return related_answers_blocks
