from typing import Iterable, Mapping, MutableMapping

from werkzeug.datastructures import ImmutableDict

from app.data_models import AnswerStore, ListStore, ProgressStore
from app.data_models.metadata_proxy import MetadataProxy
from app.questionnaire import Location, QuestionnaireSchema
from app.questionnaire.placeholder_renderer import PlaceholderRenderer
from app.survey_config.link import Link
from app.views.contexts.summary.block import Block
from app.views.contexts.summary.calculated_summary_block import CalculatedSummaryBlock
from app.views.contexts.summary.list_collector_block import ListCollectorBlock


class Group:
    def __init__(
        self,
        *,
        group_schema: Mapping,
        routing_path_block_ids: Iterable[str],
        answer_store: AnswerStore,
        list_store: ListStore,
        metadata: MetadataProxy | None,
        response_metadata: MutableMapping,
        schema: QuestionnaireSchema,
        location: Location,
        language: str,
        progress_store: ProgressStore,
        return_to: str | None,
        return_to_block_id: str | None = None,
        summary_type: str | None = None,
        view_submitted_response: bool | None = False,
    ) -> None:
        self.id = group_schema["id"]

        self.title = group_schema.get("title")
        self.location = location
        self.placeholder_text = None
        self.links: dict[str, Link] = {}

        self.blocks = self._build_blocks_and_links(
            group_schema=group_schema,
            routing_path_block_ids=routing_path_block_ids,
            answer_store=answer_store,
            list_store=list_store,
            metadata=metadata,
            response_metadata=response_metadata,
            schema=schema,
            location=self.location,
            return_to=return_to,
            progress_store=progress_store,
            language=language,
            return_to_block_id=return_to_block_id,
            view_submitted_response=view_submitted_response,
            summary_type=summary_type,
        )

        self.placeholder_renderer = PlaceholderRenderer(
            language=language,
            answer_store=answer_store,
            list_store=list_store,
            location=self.location,
            metadata=metadata,
            response_metadata=response_metadata,
            schema=schema,
            progress_store=progress_store,
        )

    # pylint: disable=too-many-locals
    def _build_blocks_and_links(
        self,
        *,
        group_schema: Mapping,
        routing_path_block_ids: Iterable[str],
        answer_store: AnswerStore,
        list_store: ListStore,
        metadata: MetadataProxy | None,
        response_metadata: MutableMapping,
        schema: QuestionnaireSchema,
        location: Location,
        return_to: str | None,
        progress_store: ProgressStore,
        language: str,
        return_to_block_id: str | None,
        view_submitted_response: bool | None = False,
        summary_type: str | None = None,
    ) -> list[dict[str, Block]]:
        blocks = []

        for block in group_schema["blocks"]:
            # the block type will only be ListRepeatingQuestion when in the context of a calculated summary or grand calculated summary
            # any other summary like section-summary will use the parent list collector instead and render items as part of the ListCollector check further down
            if block["type"] == "ListRepeatingQuestion":
                # list repeating questions aren't themselves on the path, the parent list collector is checked in ListCollectorBlock
                list_collector_block = ListCollectorBlock(
                    routing_path_block_ids=routing_path_block_ids,
                    answer_store=answer_store,
                    list_store=list_store,
                    progress_store=progress_store,
                    metadata=metadata,
                    response_metadata=response_metadata,
                    schema=schema,
                    location=location,
                    language=language,
                    return_to=return_to,
                    return_to_block_id=return_to_block_id,
                )
                repeating_question_blocks = (
                    list_collector_block.repeating_block_question_element(block)
                )
                blocks.extend(repeating_question_blocks)

            if block["id"] not in routing_path_block_ids:
                continue
            if block["type"] in [
                "Question",
                "ListCollectorDrivingQuestion",
            ]:
                blocks.extend(
                    [
                        Block(
                            block,
                            answer_store=answer_store,
                            list_store=list_store,
                            metadata=metadata,
                            response_metadata=response_metadata,
                            schema=schema,
                            location=location,
                            return_to=return_to,
                            return_to_block_id=return_to_block_id,
                            progress_store=progress_store,
                            language=language,
                        ).serialize()
                    ]
                )
            # check the summary_type as opposed to the block type
            # otherwise this gets called on section summaries as well
            elif summary_type == "GrandCalculatedSummary":
                blocks.extend(
                    [
                        CalculatedSummaryBlock(
                            block,
                            answer_store=answer_store,
                            list_store=list_store,
                            metadata=metadata,
                            response_metadata=response_metadata,
                            schema=schema,
                            location=location,
                            return_to=return_to,
                            return_to_block_id=return_to_block_id,
                            progress_store=progress_store,
                            routing_path_block_ids=routing_path_block_ids,
                        ).serialize()
                    ]
                )

            elif block["type"] == "ListCollector":
                section: ImmutableDict | None = schema.get_section(location.section_id)

                summary_item: ImmutableDict | None
                if summary_item := schema.get_summary_item_for_list_for_section(
                    # Type ignore: section id will not be optional at this point
                    section_id=section["id"],  # type: ignore
                    list_name=block["for_list"],
                ):
                    list_collector_block = ListCollectorBlock(
                        routing_path_block_ids=routing_path_block_ids,
                        answer_store=answer_store,
                        list_store=list_store,
                        progress_store=progress_store,
                        metadata=metadata,
                        response_metadata=response_metadata,
                        schema=schema,
                        location=location,
                        language=language,
                        return_to=return_to,
                    )

                    list_summary_element = list_collector_block.list_summary_element(
                        summary_item
                    )
                    blocks.extend([list_summary_element])

                    if not view_submitted_response:
                        self.links["add_link"] = Link(
                            target="_self",
                            text=list_summary_element["add_link_text"],
                            url=list_summary_element["add_link"],
                            attributes={"data-qa": "add-item-link"},
                        )

                    self.placeholder_text = list_summary_element["empty_list_text"]

        return blocks

    def serialize(self) -> Mapping:
        return self.placeholder_renderer.render(
            data_to_render={
                "id": self.id,
                "title": self.title,
                "blocks": self.blocks,
                "links": self.links,
                "placeholder_text": self.placeholder_text,
            },
            list_item_id=self.location.list_item_id if self.location else None,
        )
