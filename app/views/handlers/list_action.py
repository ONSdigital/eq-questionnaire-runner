from flask import url_for
from werkzeug.datastructures import ImmutableDict

from app.questionnaire.location import Location
from app.questionnaire.routing_path import RoutingPath
from app.views.handlers.question import Question


class ListAction(Question):
    @property
    def parent_block(self) -> ImmutableDict:
        parent_block_id = self._schema.parent_id_map[self.block["id"]]
        # Type ignore: get_block is being called with a valid block_id
        return self._schema.get_block(parent_block_id)  # type: ignore

    @property
    def parent_location(self) -> Location:
        parent_block_id = self._schema.parent_id_map[self.block["id"]]
        return Location(
            section_id=self._current_location.section_id, block_id=parent_block_id
        )

    def _get_routing_path(self) -> RoutingPath:
        """Only the section id is required, as list collectors won't be in a repeating section"""
        return self.router.routing_path(section_id=self.parent_location.section_id)

    def is_location_valid(self) -> bool:
        can_access_parent_location = self.router.can_access_location(
            self.parent_location, self._routing_path
        )

        return bool(
            can_access_parent_location
            and self._current_location.list_name == self.parent_block["for_list"]
        )

    def get_previous_location_url(self) -> str:
        if url := self.get_section_or_final_summary_url():
            return url

        block_id = self._request_args.get("previous")
        return self._get_location_url(
            block_id=block_id,
            return_to=self._return_to,
            return_to_answer_id=self._return_to_answer_id,
            return_to_block_id=self._return_to_block_id,
        )

    def get_section_or_final_summary_url(self) -> str | None:
        if (
            self._return_to == "section-summary"
            and self.router.can_display_section_summary(
                self.parent_location.section_id, self.parent_location.list_item_id
            )
        ):
            return url_for(
                "questionnaire.get_section",
                section_id=self.parent_location.section_id,
                _anchor=self._return_to_answer_id,
            )
        if self._return_to == "final-summary" and self.router.is_questionnaire_complete:
            return url_for(
                "questionnaire.submit_questionnaire", _anchor=self._return_to_answer_id
            )

    def get_next_location_url(self) -> str:
        if url := self.get_section_or_final_summary_url():
            return url

        if (
            self.router.is_block_complete(
                # Type ignore: block_id would exist at this point
                block_id=self.parent_location.block_id,  # type: ignore
                section_id=self.parent_location.section_id,
                list_item_id=self.parent_location.list_item_id,
            )
            and not self.parent_block["type"] == "ListCollectorContent"
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

    def handle_post(self) -> None:
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
        block_id: str | None = None,
        return_to: str | None = None,
        return_to_answer_id: str | None = None,
        return_to_block_id: str | None = None,
        anchor: str | None = None,
    ) -> str:
        if block_id and self._schema.is_block_valid(block_id):
            # Type ignore: the above line check that block_id exists and is valid and therefore section exists
            section_id: str = self._schema.get_section_id_for_block_id(block_id)  # type: ignore
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
