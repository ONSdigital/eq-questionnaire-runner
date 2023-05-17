from typing import Any

from flask import url_for

from app.views.handlers.list_edit_question import ListEditQuestion


class ListRepeatingBlock(ListEditQuestion):
    def __init__(self, *args: Any) -> None:
        super().__init__(*args)
        self._repeating_block_ids: list[str] = [block["id"] for block in self.parent_block["repeating_blocks"]]

    def get_next_location_url(self) -> str:
        if self._is_returning_to_section_summary():
            return self.get_section_summary_url()

        next_block_index = self._repeating_block_ids.index(self.rendered_block["id"]) + 1
        if next_block_index < len(self._repeating_block_ids):
            repeating_block_url = url_for(
                "questionnaire.block",
                list_name=self._current_location.list_name,
                list_item_id=self._current_location.list_item_id,
                block_id=self._repeating_block_ids[next_block_index],
                return_to=self._return_to,
                return_to_answer_id=self._return_to_answer_id,
                return_to_block_id=self._return_to_block_id,
            )
            return repeating_block_url

        return super().get_next_location_url()

    def handle_post(self):
        self.questionnaire_store_updater.add_completed_location(self.current_location)
        completed_block_ids = self.questionnaire_store_updater.get_completed_block_ids(self.current_location.section_id, self.current_location.list_item_id)
        if all(repeating_block_id in completed_block_ids for repeating_block_id in self._repeating_block_ids):
            self.questionnaire_store_updater.update_section_status(True, self.current_location.section_id, self.current_location.list_item_id)
        return super().handle_post()
