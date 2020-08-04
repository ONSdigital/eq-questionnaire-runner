from app.views.handlers.list_action import ListAction


class ListRemoveQuestion(ListAction):
    def is_location_valid(self):
        list_item_doesnt_exist = (
            self._current_location.list_item_id
            not in self._questionnaire_store.list_store[
                self._current_location.list_name
            ].items
        )
        is_primary = (
            self._questionnaire_store.list_store[
                self._current_location.list_name
            ].primary_person
            == self._current_location.list_item_id
        )
        if not super().is_location_valid() or list_item_doesnt_exist or is_primary:
            return False
        return True

    def get_remove_answer_option(self):
        for answer_option in self.rendered_block["question"]["answers"][0]["options"]:
            if (
                answer_option.get("action", {}).get("type")
                == "RemoveAnswersForListItem"
            ):
                return answer_option
        return None

    def handle_post(self):
        remove_answer_option = self.get_remove_answer_option()
        remove_answer_id = self.parent_block["remove_block"]["question"]["answers"][0][
            "id"
        ]

        if self.form.data[remove_answer_id] == remove_answer_option["value"]:
            list_name = self.parent_block["for_list"]
            self.questionnaire_store_updater.remove_list_item_and_answers(
                list_name, self._current_location.list_item_id
            )

        return super().handle_post()
