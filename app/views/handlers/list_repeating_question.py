from functools import cached_property

from flask import url_for

from app.questionnaire import Location
from app.views.handlers.list_edit_question import ListEditQuestion


class ListRepeatingQuestion(ListEditQuestion):
    @cached_property
    def repeating_block_ids(self) -> list[str]:
        return self._schema.list_collector_repeating_block_ids

    def get_previous_location_url(self):
        """
        return to previous location, or when return to is None, navigate to the previous repeating block
        unless this is the first repeating block, in which case, route back to the edit block
        """
        if self._is_returning_to_section_summary():
            return self.get_section_summary_url()

        if self.return_to and self.router.can_access_location(
            Location(
                section_id=self.current_location.section_id,
                block_id=self.return_to_block_id,
            ),
            routing_path=self._routing_path,
        ):
            return self._get_location_url(
                block_id=self._return_to_block_id,
                anchor=self._return_to_answer_id,
            )

        repeating_block_index = self.repeating_block_ids.index(
            self.current_location.block_id
        )
        if repeating_block_index != 0:
            previous_repeating_block_id = self.repeating_block_ids[
                repeating_block_index - 1
            ]
            return url_for(
                "questionnaire.block",
                list_name=self.current_location.list_name,
                list_item_id=self.current_location.list_item_id,
                block_id=previous_repeating_block_id,
                return_to=self._return_to,
                return_to_answer_id=self._return_to_answer_id,
                return_to_block_id=self._return_to_block_id,
            )

        edit_block = self._schema.get_edit_block_for_list_collector(
            self.parent_block["id"]
        )
        return url_for(
            "questionnaire.block",
            list_name=self.current_location.list_name,
            list_item_id=self.current_location.list_item_id,
            block_id=edit_block["id"],
            return_to=self._return_to,
            return_to_answer_id=self._return_to_answer_id,
            return_to_block_id=self._return_to_block_id,
        )

    def handle_post(self):
        self.questionnaire_store_updater.add_completed_location(self.current_location)
        if not self.get_first_incomplete_list_repeating_block_location_for_list_item(
            repeating_block_ids=self.repeating_block_ids,
            section_id=self.current_location.section_id,
            list_item_id=self.current_location.list_item_id,
            list_name=self.current_location.list_name,
        ):
            self.questionnaire_store_updater.update_section_or_repeating_blocks_progress_completion_status(
                is_complete=True,
                section_id=self.current_location.section_id,
                list_item_id=self.current_location.list_item_id,
            )

        super().handle_post()
