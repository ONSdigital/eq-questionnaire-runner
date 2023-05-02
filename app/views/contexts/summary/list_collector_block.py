from collections import defaultdict
from typing import Any, Mapping, MutableMapping, Optional

from flask import url_for
from werkzeug.datastructures import ImmutableDict

from app.data_models import AnswerStore, ProgressStore
from app.data_models.list_store import ListModel, ListStore
from app.data_models.metadata_proxy import MetadataProxy
from app.questionnaire import Location, QuestionnaireSchema
from app.questionnaire.placeholder_renderer import PlaceholderRenderer
from app.questionnaire.routing_path import RoutingPath
from app.views.contexts.list_context import ListContext
from app.views.contexts.summary.block import Block


class ListCollectorBlock:
    def __init__(
        self,
        routing_path: RoutingPath,
        answer_store: AnswerStore,
        list_store: ListStore,
        progress_store: ProgressStore,
        metadata: Optional[MetadataProxy],
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
        self._routing_path = routing_path
        self._progress_store = progress_store

    # pylint: disable=too-many-locals
    def list_summary_element(self, summary: Mapping[str, Any]) -> dict[str, Any]:
        list_collector_block = None
        (
            edit_block_id,
            remove_block_id,
            primary_person_edit_block_id,
            related_answers,
            item_label,
            item_anchor,
        ) = (None, None, None, None, None, None)
        current_list = self._list_store[summary["for_list"]]

        list_collector_blocks = list(
            self._schema.get_list_collectors_for_list(
                self._section, for_list=summary["for_list"]
            )
        )

        add_link = self._add_link(summary, list_collector_block)

        list_collector_blocks_on_path = [
            list_collector_block
            for list_collector_block in list_collector_blocks
            if list_collector_block["id"] in self._routing_path.block_ids
        ]

        list_collector_block = (
            list_collector_blocks_on_path[0]
            if list_collector_blocks_on_path
            else list_collector_blocks[0]
        )

        rendered_summary = self._placeholder_renderer.render(
            data_to_render=summary, list_item_id=self._location.list_item_id
        )

        section_id = self._section["id"]
        if list_collector_blocks_on_path:
            edit_block_id = list_collector_block["edit_block"]["id"]
            remove_block_id = list_collector_block["remove_block"]["id"]
            add_link = self._add_link(summary, list_collector_block)
            related_answers = self._get_related_answers(current_list)
            item_anchor = self._schema.get_item_anchor(section_id, current_list.name)
            item_label = self._schema.get_item_label(section_id, current_list.name)

        if len(current_list) == 1 and current_list.primary_person:
            if primary_person_block := self._schema.get_list_collector_for_list(
                self._section, for_list=summary["for_list"], primary=True
            ):
                primary_person_edit_block_id = edit_block_id = primary_person_block[
                    "add_or_edit_block"
                ]["id"]

        list_summary_context = self.list_context(
            list_collector_block["summary"],
            for_list=list_collector_block["for_list"],
            return_to="section-summary",
            edit_block_id=edit_block_id,
            remove_block_id=remove_block_id,
            primary_person_edit_block_id=primary_person_edit_block_id,
        )

        return {
            "title": rendered_summary["title"],
            "type": rendered_summary["type"],
            "add_link": add_link,
            "add_link_text": rendered_summary["add_link_text"],
            "empty_list_text": rendered_summary.get("empty_list_text"),
            "list_name": rendered_summary["for_list"],
            "related_answers": related_answers,
            "item_label": item_label,
            "item_anchor": item_anchor,
            **list_summary_context,
        }

    @property
    def list_context(self) -> ListContext:
        return ListContext(
            self._language,
            self._schema,
            self._answer_store,
            self._list_store,
            self._progress_store,
            self._metadata,
            self._response_metadata,
        )

    def _add_link(
        self,
        summary: Mapping[str, Any],
        list_collector_block: Optional[Mapping[str, Any]],
    ) -> Optional[str]:
        if list_collector_block:
            return url_for(
                "questionnaire.block",
                list_name=summary["for_list"],
                block_id=list_collector_block["add_block"]["id"],
                return_to="section-summary",
            )

        if driving_question_block := self._schema.get_driving_question_for_list(
            self._section, summary["for_list"]
        ):
            return url_for(
                "questionnaire.block",
                block_id=driving_question_block["id"],
                return_to="section-summary",
            )

    def _get_related_answers(
        self, list_model: ListModel
    ) -> Optional[dict[str, list[dict[str, Any]]]]:
        section_id = self._section["id"]

        related_answers = self._schema.get_related_answers_for_list_for_section(
            section_id=section_id, list_name=list_model.name
        )
        if not related_answers:
            return None

        related_answers_blocks = {}

        blocks = self.get_blocks_for_related_answers(related_answers)

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
                ).serialize()
                for block in blocks
            ]

            related_answers_blocks[list_id] = serialized_blocks

        return related_answers_blocks

    def get_blocks_for_related_answers(
        self, related_answers: tuple
    ) -> list[dict[str, Any]]:
        blocks = []
        answers_by_block = defaultdict(list)

        for answer in related_answers:
            answer_id = answer["identifier"]
            # block is not optional at this point
            block: Mapping = self._schema.get_block_for_answer_id(answer_id)  # type: ignore

            block_to_keep = (
                block["edit_block"] if block["type"] == "ListCollector" else block
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
