from typing import Iterable, Mapping, Type

from werkzeug.datastructures import ImmutableDict

from app.data_models.data_stores import DataStores
from app.questionnaire import QuestionnaireSchema
from app.questionnaire.placeholder_renderer import PlaceholderRenderer
from app.questionnaire.questionnaire_schema import (
    LIST_COLLECTORS_WITH_REPEATING_BLOCKS,
    is_list_collector_block_editable,
)
from app.questionnaire.return_location import ReturnLocation
from app.survey_config.link import Link
from app.utilities.types import LocationType
from app.views.contexts.summary.block import Block
from app.views.contexts.summary.calculated_summary_block import CalculatedSummaryBlock
from app.views.contexts.summary.list_collector_block import ListCollectorBlock
from app.views.contexts.summary.list_collector_content_block import (
    ListCollectorContentBlock,
)


class Group:
    def __init__(
        self,
        *,
        group_schema: Mapping,
        routing_path_block_ids: Iterable[str],
        schema: QuestionnaireSchema,
        data_stores: DataStores,
        location: LocationType,
        language: str,
        return_location: ReturnLocation,
        summary_type: str | None = None,
        view_submitted_response: bool | None = False,
    ) -> None:
        self.id = group_schema["id"]

        self.title = group_schema.get("title")
        self.location = location
        self.placeholder_text = None
        self.links: dict[str, Link] = {}
        self.data_stores = data_stores

        self.blocks = self._build_blocks_and_links(
            group_schema=group_schema,
            routing_path_block_ids=routing_path_block_ids,
            data_stores=self.data_stores,
            schema=schema,
            location=self.location,
            return_location=return_location,
            language=language,
            view_submitted_response=view_submitted_response,
            summary_type=summary_type,
        )

        self.placeholder_renderer = PlaceholderRenderer(
            language=language,
            data_stores=data_stores,
            location=self.location,
            schema=schema,
        )

    # pylint: disable=too-many-locals
    def _build_blocks_and_links(
        self,
        *,
        group_schema: Mapping,
        routing_path_block_ids: Iterable[str],
        data_stores: DataStores,
        schema: QuestionnaireSchema,
        location: LocationType,
        return_location: ReturnLocation,
        language: str,
        view_submitted_response: bool | None = False,
        summary_type: str | None = None,
    ) -> list[dict[str, Block]]:
        blocks = []

        for block in group_schema["blocks"]:
            # the block type will only be ListRepeatingQuestion when in the context of a calculated summary or grand calculated summary
            # any other summary like section-summary will use the parent list collector instead and render items as part of the ListCollector check further down
            if block["type"] == "ListRepeatingQuestion":
                # list repeating questions aren't themselves on the path, it's determined by the parent list collector
                parent_list_collector_block_id = schema.parent_id_map[block["id"]]
                if parent_list_collector_block_id not in routing_path_block_ids:
                    continue

                list_collector_block_class: Type[
                    ListCollectorBlock | ListCollectorContentBlock
                ] = (
                    ListCollectorBlock
                    if is_list_collector_block_editable(
                        # Type ignore: return types differ
                        schema.get_block(parent_list_collector_block_id)  # type: ignore
                    )
                    else ListCollectorContentBlock
                )

                list_collector_block = list_collector_block_class(
                    routing_path_block_ids=routing_path_block_ids,
                    data_stores=data_stores,
                    schema=schema,
                    location=location,
                    language=language,
                    return_location=return_location,
                )
                repeating_answer_blocks = (
                    list_collector_block.get_repeating_block_related_answer_blocks(
                        block
                    )
                )
                blocks.extend(repeating_answer_blocks)

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
                            data_stores=data_stores,
                            schema=schema,
                            location=location,
                            return_location=return_location,
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
                            data_stores=self.data_stores,
                            schema=schema,
                            location=location,
                            return_location=return_location,
                            routing_path_block_ids=routing_path_block_ids,
                        ).serialize()
                    ]
                )

            elif block["type"] in LIST_COLLECTORS_WITH_REPEATING_BLOCKS:
                section: ImmutableDict | None = schema.get_section(location.section_id)

                summary_item: ImmutableDict | None
                if summary_item := schema.get_summary_item_for_list_for_section(
                    # Type ignore: section id will not be optional at this point
                    section_id=section["id"],  # type: ignore
                    list_name=block["for_list"],
                ):
                    list_collector_block_class = (
                        ListCollectorBlock
                        if is_list_collector_block_editable(block)
                        else ListCollectorContentBlock
                    )
                    list_collector_block = list_collector_block_class(
                        data_stores=self.data_stores,
                        routing_path_block_ids=routing_path_block_ids,
                        schema=schema,
                        location=location,
                        language=language,
                        return_location=return_location,
                    )
                    list_summary_element = list_collector_block.list_summary_element(
                        summary_item
                    )
                    blocks.extend([list_summary_element])

                    if (
                        not view_submitted_response
                        and is_list_collector_block_editable(block)
                    ):
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
