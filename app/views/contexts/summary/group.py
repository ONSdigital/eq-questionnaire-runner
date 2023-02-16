from typing import Any, Mapping, Optional

from werkzeug.datastructures import ImmutableDict

from app.data_models import AnswerStore, ListStore, ProgressStore
from app.data_models.metadata_proxy import MetadataProxy
from app.questionnaire import Location, QuestionnaireSchema
from app.questionnaire.path_finder import PathFinder
from app.questionnaire.placeholder_renderer import PlaceholderRenderer
from app.questionnaire.routing_path import RoutingPath
from app.survey_config.link import Link
from app.views.contexts.summary.block import Block
from app.views.contexts.summary.list_collector_block import ListCollectorBlock


class Group:
    def __init__(
        self,
        *,
        group_schema: Mapping[str, Any],
        routing_path: RoutingPath,
        answer_store: AnswerStore,
        list_store: ListStore,
        metadata: Optional[MetadataProxy],
        response_metadata: Mapping,
        schema: QuestionnaireSchema,
        location: Optional[Location] = None,
        language: str,
        progress_store: ProgressStore,
        return_to: Optional[str],
        return_to_block_id: Optional[str] = None,
    ) -> None:
        self.id = group_schema["id"]
        self.title = group_schema.get("title")
        self.location = location
        self.placeholder_text = None
        self.links: dict[str, Link] = {}

        if self.location:
            self.blocks = self._build_blocks_and_links(
                group_schema=group_schema,
                routing_path=routing_path,
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
            )

            path_finder = PathFinder(
                schema,
                answer_store,
                list_store,
                progress_store,
                metadata,
                response_metadata,
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
                path_finder=path_finder,
            )

    # pylint: disable=too-many-locals
    def _build_blocks_and_links(
        self,
        *,
        group_schema: Mapping[str, Any],
        routing_path: RoutingPath,
        answer_store: AnswerStore,
        list_store: ListStore,
        metadata: Optional[MetadataProxy],
        response_metadata: Mapping,
        schema: QuestionnaireSchema,
        location: Location,
        return_to: Optional[str],
        progress_store: ProgressStore,
        language: str,
        return_to_block_id: Optional[str],
    ) -> list[dict[str, Block]]:
        blocks = []

        for block in group_schema["blocks"]:
            if block["id"] not in routing_path:
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
                        ).serialize()
                    ]
                )

            elif block["type"] == "ListCollector":
                section: Optional[ImmutableDict] = schema.get_section(
                    location.section_id
                )

                summary_item: Optional[ImmutableDict]
                if summary_item := schema.get_summary_item_for_list_for_section(
                    # Type ignore: section id will not be optional at this point
                    section_id=section["id"],  # type: ignore
                    list_name=block["for_list"],
                ):
                    list_collector_block = ListCollectorBlock(
                        routing_path=routing_path,
                        answer_store=answer_store,
                        list_store=list_store,
                        progress_store=progress_store,
                        metadata=metadata,
                        response_metadata=response_metadata,
                        schema=schema,
                        location=location,
                        language=language,
                    )

                    list_summary_element = list_collector_block.list_summary_element(
                        summary_item
                    )
                    blocks.extend([list_summary_element])
                    self.links["add_link"] = Link(
                        target="_self",
                        text=list_summary_element["add_link_text"],
                        url=list_summary_element["add_link"],
                        attributes={"data-qa": "add-item-link"},
                    )

                    self.placeholder_text = list_summary_element["empty_list_text"]

        return blocks

    def serialize(self) -> Mapping[str, Any]:
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
