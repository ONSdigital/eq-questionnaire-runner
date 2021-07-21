from typing import MutableMapping

from app.views.handlers.list_action import ListAction


class ListAddQuestion(ListAction):
    def is_location_valid(self):
        if not super().is_location_valid() or self._current_location.list_item_id:
            return False
        return True

    def handle_post(self):
        list_item_id = self.questionnaire_store_updater.add_list_item(
            self.parent_block["for_list"]
        )
        self.questionnaire_store_updater.update_answers(self.form.data, list_item_id)
        return super().handle_post()

    def _resolve_custom_page_title_vars(self) -> MutableMapping:
        # For list add blocks, no list item id is yet available. Instead, we resolve
        # `list_item_position` to the position in the list it would be if added.
        list_length = len(
            self._questionnaire_store.list_store[self._current_location.list_name]
        )

        return {"list_item_position": list_length + 1}
