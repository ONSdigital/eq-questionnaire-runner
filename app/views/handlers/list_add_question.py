from app.views.handlers.list_action import ListAction


class ListAddQuestion(ListAction):
    def is_location_valid(self):
        if not super().is_location_valid() or self._current_location.list_item_id:
            return False
        return True

    def handle_post(self):
        same_name_answer_ids = self.parent_block.get("same_name_answer_ids", [])

        list_item_id = self.questionnaire_store_updater.add_list_item(
            self.parent_block["for_list"]
        )
        self.questionnaire_store_updater.update_answers(self.form.data, list_item_id)

        self.questionnaire_store_updater.update_same_name_items(
            self.parent_block["for_list"], same_name_answer_ids
        )

        return super().handle_post()
