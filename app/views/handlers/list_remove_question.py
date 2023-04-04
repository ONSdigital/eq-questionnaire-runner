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
        answer_block = self._schema.get_add_block_for_list_collector(  # pylint: disable=protected-access
            self.parent_block["id"]
        )
        answer_id = self._schema.get_first_answer_id_for_block(answer_block["id"])
        self.questionnaire_store_updater._capture_block_dependencies_for_answer(  # pylint: disable=protected-access
            answer_id
        )

        answer_action = self._get_answer_action()

        if answer_action and answer_action["type"] == "RemoveListItemAndAnswers":
            list_name = self.parent_block["for_list"]
            self.questionnaire_store_updater.remove_list_item_and_answers(
                list_name, self._current_location.list_item_id
            )
            self.evaluate_and_update_section_status_on_list_change(
                self.parent_block["for_list"]
            )

        self.questionnaire_store_updater.update_progress_for_dependent_sections()

        return super().handle_post()

    def individual_response_enabled(self) -> bool:
        return (
            self.parent_block["for_list"] == self._schema.get_individual_response_list()
        )

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
