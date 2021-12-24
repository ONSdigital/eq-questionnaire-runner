from datetime import datetime, timezone
from functools import cached_property
from typing import MutableMapping, Optional, Union

from structlog import get_logger

from app.data_models import QuestionnaireStore
from app.questionnaire.location import InvalidLocationException, Location
from app.questionnaire.placeholder_renderer import PlaceholderRenderer
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.questionnaire.questionnaire_store_updater import QuestionnaireStoreUpdater
from app.questionnaire.relationship_location import RelationshipLocation
from app.questionnaire.router import Router
from app.utilities import safe_content

logger = get_logger()


class BlockHandler:
    def __init__(
        self,
        schema: QuestionnaireSchema,
        questionnaire_store: QuestionnaireStore,
        language: str,
        current_location: Union[Location, RelationshipLocation],
        request_args: MutableMapping,
        form_data: MutableMapping,
    ):
        self._schema = schema
        self._questionnaire_store = questionnaire_store
        self._language = language
        self._current_location = current_location
        self._request_args = request_args or {}
        self._form_data = form_data

        if self._current_location.block_id:
            self.block = self._schema.get_block(self._current_location.block_id)
        self._routing_path = self._get_routing_path()
        self.page_title = None
        self._return_to = request_args.get("return_to")
        self.resume = "resume" in request_args

        if not self.is_location_valid():
            raise InvalidLocationException(
                f"location {self._current_location} is not valid"
            )

    @property
    def current_location(self):
        return self._current_location

    @cached_property
    def questionnaire_store_updater(self):
        return QuestionnaireStoreUpdater(
            self._current_location,
            self._schema,
            self._questionnaire_store,
            self.block.get("question"),
        )

    @cached_property
    def placeholder_renderer(self):
        return PlaceholderRenderer(
            self._language,
            answer_store=self._questionnaire_store.answer_store,
            list_store=self._questionnaire_store.list_store,
            metadata=self._questionnaire_store.metadata,
            response_metadata=self._questionnaire_store.response_metadata,
            schema=self._schema,
            location=self._current_location,
        )

    @cached_property
    def router(self):
        return Router(
            schema=self._schema,
            answer_store=self._questionnaire_store.answer_store,
            list_store=self._questionnaire_store.list_store,
            progress_store=self._questionnaire_store.progress_store,
            metadata=self._questionnaire_store.metadata,
            response_metadata=self._questionnaire_store.response_metadata,
        )

    def is_location_valid(self):
        return self.router.can_access_location(
            self._current_location, self._routing_path
        )

    def get_previous_location_url(self):
        return self.router.get_previous_location_url(
            self._current_location, self._routing_path, self._return_to
        )

    def get_next_location_url(self):
        return self.router.get_next_location_url(
            self._current_location, self._routing_path, self._return_to
        )

    def handle_post(self):
        self._set_started_at_metadata()
        self.questionnaire_store_updater.add_completed_location()
        self._update_section_completeness()
        self.questionnaire_store_updater.save()

    def _get_routing_path(self):
        return self.router.routing_path(
            section_id=self._current_location.section_id,
            list_item_id=self._current_location.list_item_id,
        )

    def _update_section_completeness(
        self, location: Optional[Union[Location, RelationshipLocation]] = None
    ):
        location = location or self._current_location

        self.questionnaire_store_updater.update_section_status(
            is_complete=self.router.is_path_complete(self._routing_path),
            section_id=location.section_id,
            list_item_id=location.list_item_id,
        )

    def _set_started_at_metadata(self):
        response_metadata = self._questionnaire_store.response_metadata
        if not response_metadata.get("started_at"):
            started_at = datetime.now(timezone.utc).isoformat()
            logger.info("Survey started", started_at=started_at)
            response_metadata["started_at"] = started_at

    def _get_safe_page_title(self, page_title):
        page_title = self._schema.get_single_string_value(page_title)
        return safe_content(page_title)

    def _resolve_custom_page_title_vars(self) -> MutableMapping:
        list_item_position = self._questionnaire_store.list_store.list_item_position(
            self.current_location.list_name, self.current_location.list_item_id
        )
        return {"list_item_position": list_item_position}

    def _set_page_title(self, page_title):
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
