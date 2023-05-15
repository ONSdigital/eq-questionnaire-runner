from typing import Any, MutableMapping

from flask import url_for

from app.views.handlers.list_action import ListAction


class ListAddQuestion(ListAction):
    def __init__(self, *args: Any):
        self._list_item_id: str | None = None
        super().__init__(*args)

    def is_location_valid(self):
        if not super().is_location_valid() or self._current_location.list_item_id:
            return False
        return True

    def get_next_location_url(self):
        if self._list_item_id and (
            repeating_blocks := self.parent_block.get("repeating_blocks")
        ):
            repeating_block_url = url_for(
                "questionnaire.block",
                list_name=self.parent_block["for_list"],
                list_item_id=self._list_item_id,
                block_id=repeating_blocks[0]["id"],
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

    def handle_post(self):
        # Ensure the section is in progress when user adds an item
        self._list_item_id = self.questionnaire_store_updater.add_list_item(
            self.parent_block["for_list"]
        )
        self.questionnaire_store_updater.add_list_item_progress(self._list_item_id, self.parent_block.get("repeating_blocks"))

        # Clear the answer from the confirmation question on the list collector question
        answer_ids_to_remove = self._schema.get_answer_ids_for_block(
            self.parent_location.block_id
        )
        self.questionnaire_store_updater.remove_answers(answer_ids_to_remove)
        self.questionnaire_store_updater.remove_completed_location(self.parent_location)

        # pylint: disable=no-member
        # wtforms Form parents are not discoverable in the 2.3.3 implementation
        self.questionnaire_store_updater.update_answers(
            self.form.data, self._list_item_id
        )

        self.evaluate_and_update_section_status_on_list_change(
            self.parent_block["for_list"]
        )

        return super().handle_post()

    def _resolve_custom_page_title_vars(self) -> MutableMapping:
        # For list add blocks, no list item id is yet available. Instead, we resolve
        # `list_item_position` to the position in the list it would be if added.
        list_length = len(
            self._questionnaire_store.list_store[self._current_location.list_name]  # type: ignore
        )

        return {"list_item_position": list_length + 1}
