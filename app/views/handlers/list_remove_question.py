from app.views.handlers import individual_response_url
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

    def handle_post(self):
        answer_action = self._get_answer_action()

        if answer_action and answer_action["type"] == "RemoveListItemAndAnswers":
            same_name_answer_ids = self.parent_block.get("same_name_answer_ids", [])
            list_name = self.parent_block["for_list"]
            self.questionnaire_store_updater.remove_list_item_and_answers(
                list_name, self._current_location.list_item_id
            )
            self.questionnaire_store_updater.update_same_name_items(
                self.parent_block["for_list"], same_name_answer_ids
            )

        return super().handle_post()

    def individual_response_enabled(self) -> bool:
        if self._schema.json.get("individual_response"):
            return True
        return False

    def get_context(self):
        context = super().get_context()
        context["individual_response_enabled"] = self.individual_response_enabled()
        context["individual_response_url"] = individual_response_url(
            self._schema.get_individual_response_list(),
            self._current_location.list_item_id,
            self._questionnaire_store,
            journey="remove-person",
        )
        return context
