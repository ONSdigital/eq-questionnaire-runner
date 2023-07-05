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

    def get_next_location_url(self):
        if self._is_returning_to_section_summary():
            return self.get_section_summary_url()

        if url := self._get_first_incomplete_repeating_block_url():
            return url

        return super().get_next_location_url()

    def handle_post(self):
        # pylint: disable=no-member
        # wtforms Form parents are not discoverable in the 2.3.3 implementation
        self.questionnaire_store_updater.update_answers(self.form.data)

        return super().handle_post()
