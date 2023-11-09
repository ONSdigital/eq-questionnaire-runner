from app.views.handlers import individual_response_url
from app.views.handlers.list_action import ListAction


class ListRemoveQuestion(ListAction):
    def is_location_valid(self) -> bool:
        list_item_doesnt_exist = (
            self._current_location.list_item_id
            not in self._questionnaire_store.list_store[
                # Type ignore: list_name will exist within the remove block
                self._current_location.list_name  # type: ignore
            ].items
        )
        is_primary = (
            self._questionnaire_store.list_store[
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
            self.questionnaire_store_updater.capture_dependencies_for_list_change(
                list_name
            )

        return super().handle_post()

    def individual_response_enabled(self) -> bool:
        # Type ignore: we know "for_list" will be a string
        return self.parent_block["for_list"] == self._schema.get_individual_response_list()  # type: ignore

    def get_context(self) -> dict:
        context: dict = super().get_context()
        context["individual_response_enabled"] = self.individual_response_enabled()
        context["individual_response_url"] = individual_response_url(
            self._schema.get_individual_response_list(),
            # Type ignore: in a list so we know this cannot be None
            self._current_location.list_item_id,  # type: ignore
            self._questionnaire_store,
            journey="remove-person",
        )
        return context
