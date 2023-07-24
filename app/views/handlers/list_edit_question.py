from app.views.handlers.list_action import ListAction


class ListEditQuestion(ListAction):
    def is_location_valid(self) -> bool:
        list_item_doesnt_exist = (
            self._current_location.list_item_id
            not in self._questionnaire_store.list_store[
                # Type ignore: list_name/list_item_id already exist
                self._current_location.list_name  # type: ignore
            ].items
        )
        if not super().is_location_valid() or list_item_doesnt_exist:
            return False
        return True

    def handle_post(self) -> None:
        # pylint: disable=no-member
        # wtforms Form parents are not discoverable in the 2.3.3 implementation
        self.questionnaire_store_updater.update_answers(self.form.data)

        return super().handle_post()
