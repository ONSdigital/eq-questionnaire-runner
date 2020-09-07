from app.views.handlers.list_action import ListAction


class ListEditQuestion(ListAction):
    def is_location_valid(self):
        list_item_doesnt_exist = (
            self._current_location.list_item_id
            not in self._questionnaire_store.list_store[
                self._current_location.list_name
            ].items
        )
        if not super().is_location_valid() or list_item_doesnt_exist:
            return False
        return True

    def handle_post(self):
        same_name_answer_ids = self.parent_block.get("same_name_answer_ids", False)

        self.questionnaire_store_updater.update_answers(self.form.data)

        if same_name_answer_ids:
            self.questionnaire_store_updater.update_same_name_items(
                self.parent_block["for_list"], same_name_answer_ids
            )

        return super().handle_post()
