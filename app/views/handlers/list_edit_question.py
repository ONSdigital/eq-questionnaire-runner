from flask import url_for

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
        """
        Unless editing from the summary page, If there are repeating blocks and not all are complete, go to the next one
        """
        if self._is_returning_to_section_summary():
            return self.get_section_summary_url()

        if first_incomplete_block := self.get_first_incomplete_repeating_block_location_for_list_item(
            repeating_block_ids=self._schema.repeating_block_ids,
            section_id=self.current_location.section_id,
            list_item_id=self.current_location.list_item_id,
            list_name=self.current_location.list_name,
        ):
            return url_for(
                "questionnaire.block",
                list_name=first_incomplete_block.list_name,
                list_item_id=first_incomplete_block.list_item_id,
                block_id=first_incomplete_block.block_id,
                return_to=self._return_to,
                return_to_answer_id=self._return_to_answer_id,
                return_to_block_id=self._return_to_block_id,
            )

        return super().get_next_location_url()

    def handle_post(self):
        # pylint: disable=no-member
        # wtforms Form parents are not discoverable in the 2.3.3 implementation
        self.questionnaire_store_updater.update_answers(self.form.data)

        return super().handle_post()
