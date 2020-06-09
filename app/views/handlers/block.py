from datetime import datetime
from functools import cached_property
from typing import Optional

from structlog import get_logger

from app.questionnaire.location import InvalidLocationException, Location
from app.questionnaire.placeholder_renderer import PlaceholderRenderer
from app.questionnaire.questionnaire_store_updater import QuestionnaireStoreUpdater
from app.questionnaire.router import Router

logger = get_logger()


class BlockHandler:
    def __init__(
        self, schema, questionnaire_store, language, current_location, request_args
    ):
        self._schema = schema
        self._questionnaire_store = questionnaire_store
        self._language = language
        self._current_location = current_location
        self._request_args = request_args or {}
        self.block = self._schema.get_block(current_location.block_id)

        self._routing_path = self._get_routing_path()
        self.form = None
        self.page_title = None
        self._return_to_summary = "return_to_summary" in request_args
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
            schema=self._schema,
            answer_store=self._questionnaire_store.answer_store,
            metadata=self._questionnaire_store.metadata,
            location=self._current_location,
            list_store=self._questionnaire_store.list_store,
        )

    @cached_property
    def router(self):
        return Router(
            schema=self._schema,
            answer_store=self._questionnaire_store.answer_store,
            list_store=self._questionnaire_store.list_store,
            progress_store=self._questionnaire_store.progress_store,
            metadata=self._questionnaire_store.metadata,
        )

    def is_location_valid(self):
        return self.router.can_access_location(
            self._current_location, self._routing_path
        )

    def get_previous_location_url(self):
        return self.router.get_previous_location_url(
            self._current_location, self._routing_path
        )

    def get_next_location_url(self):
        return self.router.get_next_location_url(
            self._current_location, self._routing_path, self._return_to_summary
        )

    def handle_post(self):
        self.questionnaire_store_updater.add_completed_location()
        self._update_section_completeness()
        self.questionnaire_store_updater.save()

    def set_started_at_metadata(self):
        collection_metadata = self._questionnaire_store.collection_metadata
        if not collection_metadata.get("started_at"):
            started_at = datetime.utcnow().isoformat()

            logger.info(
                "Survey started. Writing started_at time to collection metadata",
                started_at=started_at,
            )

            collection_metadata["started_at"] = started_at

    def _get_routing_path(self):
        return self.router.routing_path(
            section_id=self._current_location.section_id,
            list_item_id=self._current_location.list_item_id,
        )

    def _update_section_completeness(self, location: Optional[Location] = None):
        location = location or self._current_location

        self.questionnaire_store_updater.update_section_status(
            is_complete=self.router.is_path_complete(self._routing_path),
            section_id=location.section_id,
            list_item_id=location.list_item_id,
        )
