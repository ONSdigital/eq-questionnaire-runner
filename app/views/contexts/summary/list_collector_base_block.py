from collections import defaultdict
from typing import Iterable, Mapping, MutableMapping, Sequence

from werkzeug.datastructures import ImmutableDict

from app.data_models import AnswerStore, ProgressStore, SupplementaryDataStore
from app.data_models.list_store import ListModel, ListStore
from app.data_models.metadata_proxy import MetadataProxy
from app.questionnaire import Location, QuestionnaireSchema
from app.questionnaire.placeholder_renderer import PlaceholderRenderer
from app.questionnaire.questionnaire_schema import is_list_collector_block_editable
from app.views.contexts import list_context
from app.views.contexts.summary.block import Block


class ListCollectorBaseBlock:
    def __init__(
        self,
        *,
        routing_path_block_ids: Iterable[str],
        answer_store: AnswerStore,
        list_store: ListStore,
        progress_store: ProgressStore,
        metadata: MetadataProxy | None,
        response_metadata: MutableMapping,
        schema: QuestionnaireSchema,
        location: Location,
        language: str,
        supplementary_data_store: SupplementaryDataStore,
        return_to: str | None,
        return_to_block_id: str | None = None,
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
            supplementary_data_store=supplementary_data_store,
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
        self._supplementary_data_store = supplementary_data_store
        self._return_to = return_to
        self._return_to_block_id = return_to_block_id

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
            self._supplementary_data_store,
        )

    def _list_collector_block_on_path(self, for_list: str) -> list:
        list_collector_blocks = list(
            self._schema.get_list_collectors_for_list(self._section, for_list=for_list)
        )

        return [
            list_collector_block
            for list_collector_block in list_collector_blocks
            if list_collector_block["id"] in self._routing_path_block_ids
        ]

    def _list_collector_block(
        self, for_list: str, list_collector_blocks_on_path: list
    ) -> ImmutableDict:
        list_collector_blocks = list(
            self._schema.get_list_collectors_for_list(self._section, for_list=for_list)
        )
        # Type ignore: self._schema.get_list_collectors_for_list can return None
        return (  # type: ignore
            list_collector_blocks_on_path[0]
            if list_collector_blocks_on_path
            else list_collector_blocks[0]
        )

    def _get_related_answer_blocks_by_list_item_id(
        self, *, list_model: ListModel, repeating_blocks: Sequence[ImmutableDict]
    ) -> dict[str, list[dict]] | None:
        section_id = self._section["id"]

        related_answers = self._schema.get_related_answers_for_list_for_section(
            section_id=section_id, list_name=list_model.name
        )

        blocks: list[dict | ImmutableDict] = []

        if related_answers:
            blocks += self._get_blocks_for_related_answers(related_answers)

        if len(list_model):
            blocks += repeating_blocks

        if not blocks:
            return None

        related_answers_blocks = {}

        for list_id in list_model:
            serialized_blocks = [
                # related answers for repeating blocks may use placeholders, so each block needs rendering here
                self._placeholder_renderer.render(
                    data_to_render=Block(
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
                        return_to=self._return_to,
                        return_to_block_id=self._return_to_block_id,
                        progress_store=self._progress_store,
                        supplementary_data_store=self._supplementary_data_store,
                        language=self._language,
                    ).serialize(),
                    list_item_id=list_id,
                )
                for block in blocks
            ]

            related_answers_blocks[list_id] = serialized_blocks

        return related_answers_blocks

    def _get_blocks_for_related_answers(self, related_answers: tuple) -> list[dict]:
        blocks = []
        answers_by_block = defaultdict(list)

        for answer in related_answers:
            answer_id = answer["identifier"]
            # block is not optional at this point
            block: Mapping = self._schema.get_block_for_answer_id(answer_id)  # type: ignore

            block_to_keep = (
                block["edit_block"]
                if is_list_collector_block_editable(block)
                else block
            )
            answers_by_block[block_to_keep].append(answer_id)

        for immutable_block, answer_ids in answers_by_block.items():
            mutable_block = self._schema.get_mutable_deepcopy(immutable_block)

            # We need to filter out answers for both variants and normal questions
            for variant_or_block in mutable_block.get(
                "question_variants", [mutable_block]
            ):
                answers = [
                    answer
                    for answer in variant_or_block["question"].get("answers", {})
                    if answer["id"] in answer_ids
                ]
                # Mutate the answers to only keep the related answers
                variant_or_block["question"]["answers"] = answers

            blocks.append(mutable_block)

        return blocks

    def get_repeating_block_related_answer_blocks(
        self, block: ImmutableDict
    ) -> list[dict]:
        """
        Given a repeating block question to render,
        return the list of rendered question blocks for each list item id
        """
        list_name = self._schema.list_names_by_list_repeating_block_id[block["id"]]
        list_model = self._list_store[list_name]
        blocks: list[dict] = []
        if answer_blocks_by_list_item_id := self._get_related_answer_blocks_by_list_item_id(
            list_model=list_model, repeating_blocks=[block]
        ):
            for answer_blocks in answer_blocks_by_list_item_id.values():
                blocks.extend(answer_blocks)
        return blocks
