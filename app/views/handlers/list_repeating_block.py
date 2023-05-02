from flask import url_for

from app.views.handlers.list_edit_question import ListEditQuestion


class ListRepeatingBlock(ListEditQuestion):

    def get_next_location_url(self) -> str:
        # Get parent
        # Find repeating_sections
        # Find index of this block id
        # If next exists in repeating_sections go to that
        # else go to parent (list collector)
        repeating_block_ids = [block["id"] for block in self.parent_block["repeating_blocks"]]
        next_block_index = repeating_block_ids.index(self.rendered_block["id"]) + 1
        if next_block_index < len(repeating_block_ids):
            repeating_block_url = url_for(
                "questionnaire.block",
                list_name=self._current_location.list_name,
                list_item_id=self._current_location.list_item_id,
                block_id=repeating_block_ids[next_block_index],
                return_to=self._return_to,
                return_to_answer_id=self._return_to_answer_id,
                return_to_block_id=self._return_to_block_id,
            )
            return repeating_block_url

        return self.parent_location.url(
            return_to=self._return_to,
            return_to_answer_id=self._return_to_answer_id,
            return_to_block_id=self._return_to_block_id,
        )
