from functools import cached_property

from flask import url_for

from app.views.handlers.list_edit_question import ListEditQuestion


class ListRepeatingBlock(ListEditQuestion):

    @cached_property
    def repeating_block_ids(self) -> list[str]:
        return [block["id"] for block in self.parent_block["repeating_blocks"]]

    def get_next_location_url(self) -> str:
        if self._is_returning_to_section_summary():
            return self.get_section_summary_url()

        if first_incomplete_block := self.get_first_incomplete_repeating_block_location_for_list_item(repeating_block_ids=self.repeating_block_ids,
                                                                                                      section_id=self.current_location.section_id,
                                                                                                      list_item_id=self.current_location.list_item_id,
                                                                                                      list_name=self.current_location.list_name):
            repeating_block_url = url_for(
                "questionnaire.block",
                list_name=first_incomplete_block.list_name,
                list_item_id=first_incomplete_block.list_item_id,
                block_id=first_incomplete_block.block_id,
                return_to=self._return_to,
                return_to_answer_id=self._return_to_answer_id,
                return_to_block_id=self._return_to_block_id,
            )
            return repeating_block_url

        return super().get_next_location_url()

    def handle_post(self):
        self.questionnaire_store_updater.add_completed_location(self.current_location)
        if not self.get_first_incomplete_repeating_block_location_for_list_item(repeating_block_ids=self.repeating_block_ids,
                                                                                section_id=self.current_location.section_id,
                                                                                list_item_id=self.current_location.list_item_id,
                                                                                list_name=self.current_location.list_name):
            self.questionnaire_store_updater.update_section_status(True, self.current_location.section_id, self.current_location.list_item_id)
        return super().handle_post()
