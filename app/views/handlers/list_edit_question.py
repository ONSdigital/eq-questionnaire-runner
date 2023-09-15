from functools import cached_property

from flask import url_for

from app.views.handlers.list_action import ListAction


class ListEditQuestion(ListAction):
    @cached_property
    def repeating_block_ids(self) -> list[str]:
        return [
            repeating_block["id"]
            for repeating_block in self.parent_block.get("repeating_blocks", [])
        ]

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

    def get_next_location_url(self) -> str:
        """
        Unless editing from the summary page, If there are repeating blocks and not all are complete, go to the next one
        """
        if url := self.get_section_or_final_summary_url():
            return url

        if first_incomplete_block := self.get_first_incomplete_list_repeating_block_location_for_list_item(
            repeating_block_ids=self.repeating_block_ids,
            section_key=self.current_location.section_key,
            # Type ignore: list_name will exist at this point
            list_name=self.current_location.list_name,  # type: ignore
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

    def handle_post(self) -> None:
        # pylint: disable=no-member
        # wtforms Form parents are not discoverable in the 2.3.3 implementation
        self.questionnaire_store_updater.update_answers(self.form.data)

        return super().handle_post()
