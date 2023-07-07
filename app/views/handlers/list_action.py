from flask import url_for

from app.questionnaire.location import Location
from app.views.handlers.question import Question


class ListAction(Question):
    @property
    def parent_block(self):
        parent_block_id = self._schema.parent_id_map[self.block["id"]]
        return self._schema.get_block(parent_block_id)

    @property
    def parent_location(self):
        parent_block_id = self._schema.parent_id_map[self.block["id"]]
        return Location(
            section_id=self._current_location.section_id, block_id=parent_block_id
        )

    def _get_routing_path(self):
        return self.router.routing_path(
            section_id=self.parent_location.section_id,
            list_item_id=self.parent_location.list_item_id,
        )

    def is_location_valid(self):
        can_access_parent_location = self.router.can_access_location(
            self.parent_location, self._routing_path
        )

        if (
            not can_access_parent_location
            or self._current_location.list_name != self.parent_block["for_list"]
        ):
            return False

        return True

    def get_previous_location_url(self):
        if self._is_returning_to_section_summary():
            return self.get_section_summary_url()

        block_id = self._request_args.get("previous")
        return self._get_location_url(
            block_id=block_id,
            return_to=self._return_to,
            return_to_answer_id=self._return_to_answer_id,
            return_to_block_id=self._return_to_block_id,
        )

    def get_section_summary_url(self):
        return url_for(
            "questionnaire.get_section", section_id=self.parent_location.section_id
        )

    def get_next_location_url(self):
        if self._is_returning_to_section_summary():
            return self.get_section_summary_url()

        if self.router.is_block_complete(
            block_id=self.parent_location.block_id,
            section_id=self.parent_location.section_id,
            list_item_id=self.parent_location.list_item_id,
        ):
            return self.router.get_next_location_url(
                self.parent_location,
                self._routing_path,
                self._return_to,
                self._return_to_answer_id,
                self._return_to_block_id,
            )

        return self.parent_location.url(
            return_to=self._return_to,
            return_to_answer_id=self._return_to_answer_id,
            return_to_block_id=self._return_to_block_id,
        )

    def handle_post(self):
        self.questionnaire_store_updater.update_same_name_items(
            self.parent_block["for_list"],
            self.parent_block.get("same_name_answer_ids"),
        )

        if self.questionnaire_store_updater.is_dirty():
            self._routing_path = self._get_routing_path()
            self.questionnaire_store_updater.remove_dependent_blocks_and_capture_dependent_sections()
            self.questionnaire_store_updater.update_progress_for_dependent_sections()
            self.questionnaire_store_updater.save()

    def _get_location_url(
        self,
        *,
        block_id=None,
        return_to=None,
        return_to_answer_id=None,
        return_to_block_id=None,
        anchor=None,
    ):
        if block_id and self._schema.is_block_valid(block_id):
            section_id = self._schema.get_section_id_for_block_id(block_id)
            return Location(section_id=section_id, block_id=block_id).url(
                return_to=return_to,
                return_to_answer_id=return_to_answer_id,
                return_to_block_id=return_to_block_id,
                _anchor=anchor,
            )

        return self.parent_location.url(
            return_to=return_to,
            return_to_answer_id=return_to_answer_id,
            return_to_block_id=return_to_block_id,
            _anchor=anchor,
        )

    def _is_returning_to_section_summary(self) -> bool:
        return (
            self._return_to == "section-summary"
            and self.router.can_display_section_summary(
                self.parent_location.section_id, self.parent_location.list_item_id
            )
        )
