from app.views.handlers.list_action import ListAction


class ListRemoveQuestion(ListAction):
    def is_location_valid(self) -> bool:
        list_item_doesnt_exist = (
            self._current_location.list_item_id
            not in self._questionnaire_store.data_stores.list_store[
                # Type ignore: list_name will exist within the remove block
                self._current_location.list_name  # type: ignore
            ].items
        )
        is_primary = (
            self._questionnaire_store.data_stores.list_store[
                # Type ignore: list_name will exist within the remove block
                self._current_location.list_name  # type: ignore
            ].primary_person
            == self._current_location.list_item_id
        )
        if not super().is_location_valid() or list_item_doesnt_exist or is_primary:
            return False
        return True

    def handle_post(self) -> None:
        answer_action = self._get_answer_action()

        if answer_action and answer_action["type"] == "RemoveListItemAndAnswers":
            list_name = self.parent_block["for_list"]
            self.questionnaire_store_updater.remove_list_item_data(
                # Type ignore: list_item_id will exist within the remove block
                list_name,
                self._current_location.list_item_id,  # type: ignore
            )
            # This will result in any list collector content blocks using this list to require revisiting. This is currently the expected behaviour.
            self.questionnaire_store_updater.capture_dependencies_for_list_change(
                list_name
            )

        return super().handle_post()
