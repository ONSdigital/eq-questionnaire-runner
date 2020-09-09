from datetime import datetime
from functools import cached_property
from typing import Mapping, Optional

from structlog import get_logger

from app.data_models import QuestionnaireStore
from app.helpers.template_helpers import safe_content
from app.questionnaire.location import InvalidLocationException, Location
from app.questionnaire.placeholder_renderer import PlaceholderRenderer
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.questionnaire.questionnaire_store_updater import QuestionnaireStoreUpdater
from app.questionnaire.router import Router

logger = get_logger()


class BlockHandler:
    def __init__(
        self,
        schema: QuestionnaireSchema,
        questionnaire_store: QuestionnaireStore,
        language: str,
        current_location: Location,
        request_args: Mapping,
        form_data: Mapping,
    ):
        self._schema = schema
        self._questionnaire_store = questionnaire_store
        self._language = language
        self._current_location = current_location
        self._request_args = request_args or {}
        self._form_data = form_data
        self.block = self._schema.get_block(current_location.block_id)

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

    def _update_section_completeness(self, location: Optional[Location] = None):
        location = location or self._current_location

        self.questionnaire_store_updater.update_section_status(
            is_complete=self.router.is_path_complete(self._routing_path),
            section_id=location.section_id,
            list_item_id=location.list_item_id,
        )

    def _set_started_at_metadata(self):
        collection_metadata = self._questionnaire_store.collection_metadata
        if not collection_metadata.get("started_at"):
            started_at = datetime.utcnow().isoformat()
            logger.info("Survey started", started_at=started_at)
            collection_metadata["started_at"] = started_at

    def _get_safe_page_title(self, page_title):
        page_title = self._schema.get_single_string_value(page_title)
        title = self._schema.json["title"]

        return safe_content(f"{page_title} - {title}")

    def _resolve_custom_page_title_vars(self, for_list: str) -> Mapping:
        page_title_vars = {"list_item_id": None, "to_list_item_id": None}

        if list_item_id := self.current_location.list_item_id:
            list_item_position = (
                self._questionnaire_store.list_store.list_item_position(
                    for_list, list_item_id
                )
            )
            page_title_vars["list_item_index"] = list_item_position

            try:
                if to_list_item_index := self.current_location.to_list_item_id:
                    page_title_vars[
                        "to_list_item_index"
                    ] = self._questionnaire_store.list_store.list_item_position(
                        for_list, to_list_item_index
                    )
            except AttributeError:
                pass

        return page_title_vars
