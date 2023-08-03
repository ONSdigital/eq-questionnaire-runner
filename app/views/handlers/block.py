from datetime import datetime, timezone
from functools import cached_property
from typing import Mapping, MutableMapping, Optional, Union

from structlog import get_logger
from werkzeug.datastructures import ImmutableDict, ImmutableMultiDict

from app.data_models import QuestionnaireStore
from app.questionnaire.location import InvalidLocationException, Location
from app.questionnaire.placeholder_renderer import PlaceholderRenderer
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.questionnaire.questionnaire_store_updater import QuestionnaireStoreUpdater
from app.questionnaire.relationship_location import RelationshipLocation
from app.questionnaire.router import Router
from app.questionnaire.routing_path import RoutingPath
from app.utilities import safe_content
from app.utilities.types import LocationType

logger = get_logger()


class BlockHandler:
    def __init__(
        self,
        schema: QuestionnaireSchema,
        questionnaire_store: QuestionnaireStore,
        language: str,
        current_location: Location,
        request_args: MutableMapping,
        form_data: ImmutableMultiDict,
    ):
        self._schema = schema
        self._questionnaire_store = questionnaire_store
        self._language = language
        self._current_location = current_location
        self._request_args = request_args or {}
        self._form_data = form_data

        if self._current_location.block_id:
            # Type ignore: Block has to exist at this point. Block existence is checked beforehand in block_factory.py
            self.block: ImmutableDict = self._schema.get_block(self._current_location.block_id)  # type: ignore
        self._routing_path = self._get_routing_path()
        self.page_title: Optional[str] = None
        self._return_to = request_args.get("return_to")
        self._return_to_answer_id = request_args.get("return_to_answer_id")
        self._return_to_block_id = request_args.get("return_to_block_id")
        self.resume = "resume" in request_args

        if not self.is_location_valid():
            raise InvalidLocationException(
                f"location {self._current_location} is not valid"
            )

    @property
    def current_location(self) -> LocationType:
        return self._current_location

    @property
    def return_to(self) -> str | None:
        return self._return_to

    @property
    def return_to_block_id(self) -> str | None:
        return self._return_to_block_id

    @cached_property
    def questionnaire_store_updater(self) -> QuestionnaireStoreUpdater:
        return QuestionnaireStoreUpdater(
            self._current_location,
            self._schema,
            self._questionnaire_store,
            self.router,
            self.block.get("question"),
        )

    @cached_property
    def placeholder_renderer(self) -> PlaceholderRenderer:
        return PlaceholderRenderer(
            self._language,
            answer_store=self._questionnaire_store.answer_store,
            list_store=self._questionnaire_store.list_store,
            metadata=self._questionnaire_store.metadata,
            response_metadata=self._questionnaire_store.response_metadata,
            schema=self._schema,
            location=self._current_location,
            progress_store=self._questionnaire_store.progress_store,
            supplementary_data_store=self._questionnaire_store.supplementary_data_store,
        )

    @cached_property
    def router(self) -> Router:
        return Router(
            schema=self._schema,
            answer_store=self._questionnaire_store.answer_store,
            list_store=self._questionnaire_store.list_store,
            progress_store=self._questionnaire_store.progress_store,
            metadata=self._questionnaire_store.metadata,
            response_metadata=self._questionnaire_store.response_metadata,
            supplementary_data_store=self._questionnaire_store.supplementary_data_store,
        )

    def is_location_valid(self) -> bool:
        return self.router.can_access_location(
            self._current_location, self._routing_path
        )

    def get_previous_location_url(self) -> str | None:
        return self.router.get_previous_location_url(
            self._current_location,
            self._routing_path,
            self._return_to,
            self._return_to_answer_id,
            self._return_to_block_id,
        )

    def get_next_location_url(self) -> str:
        return self.router.get_next_location_url(
            self._current_location,
            self._routing_path,
            self._return_to,
            self._return_to_answer_id,
            self._return_to_block_id,
        )

    def handle_post(self) -> None:
        self._set_started_at_metadata()
        self.questionnaire_store_updater.add_completed_location()
        self.questionnaire_store_updater.remove_dependent_blocks_and_capture_dependent_sections()
        self._update_section_completeness()
        self.questionnaire_store_updater.update_progress_for_dependent_sections()
        self.questionnaire_store_updater.save()

    def _get_routing_path(self) -> RoutingPath:
        return self.router.routing_path(
            section_id=self._current_location.section_id,
            list_item_id=self._current_location.list_item_id,
        )

    def _update_section_completeness(
        self, location: Optional[Union[Location, RelationshipLocation]] = None
    ) -> None:
        location = location or self._current_location

        self.questionnaire_store_updater.update_section_or_repeating_blocks_progress_completion_status(
            is_complete=self.router.is_path_complete(self._routing_path),
            section_id=location.section_id,
            list_item_id=location.list_item_id,
        )

    def _set_started_at_metadata(self) -> str | None:
        response_metadata = self._questionnaire_store.response_metadata
        if not response_metadata.get("started_at"):
            started_at = datetime.now(timezone.utc).isoformat()
            logger.info("Survey started", started_at=started_at)
            response_metadata["started_at"] = started_at

    def _get_safe_page_title(self, page_title: Mapping | str) -> str:
        page_title = self._schema.get_single_string_value(page_title)
        return safe_content(page_title)

    def _resolve_custom_page_title_vars(self) -> MutableMapping:
        # Type ignore: list_item_id and list_name are populated at this stage
        list_item_position = self._questionnaire_store.list_store.list_item_position(
            self.current_location.list_name,  # type: ignore
            self.current_location.list_item_id,  # type: ignore
        )
        return {"list_item_position": list_item_position}

    def _set_page_title(self, page_title: str | None) -> str | None:
        if not page_title:
            return None

        section_repeating_page_title = (
            self._schema.get_repeating_page_title_for_section(
                self._current_location.section_id
            )
        )
        if section_repeating_page_title:
            page_title = f"{page_title}: {section_repeating_page_title}"

        if (
            self._current_location.list_item_id
            or self.block["type"] == "ListAddQuestion"
        ):
            page_title_vars = self._resolve_custom_page_title_vars()
            page_title = page_title.format(**page_title_vars)

        self.page_title = page_title
