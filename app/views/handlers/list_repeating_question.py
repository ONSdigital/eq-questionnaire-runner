from functools import cached_property

from flask import url_for

from app.views.handlers.list_action import ListAction


class ListRepeatingQuestion(ListAction):
    @cached_property
    def repeating_block_ids(self) -> list[str]:
        return self._schema.get_repeating_block_ids()

    def get_next_location_url(self) -> str:
        if self._is_returning_to_section_summary():
            return self.get_section_summary_url()

        if first_incomplete_location := self.get_first_incomplete_repeating_block_url(
            self.current_location.list_item_id
        ):
            return first_incomplete_location

        if (
            not first_incomplete_location
            and self.parent_block["type"] == "ListCollectorContent"
            and self._questionnaire_store.progress_store.is_section_or_repeating_blocks_progress_complete(
                section_id=self.current_location.section_id,
                list_item_id=self._current_location.list_item_id,
            )
        ):
            return url_for(
                "questionnaire.block",
                block_id=self.parent_block["id"],
                return_to=self._return_to,
                return_to_answer_id=self._return_to_answer_id,
                return_to_block_id=self._return_to_block_id,
            )

        return super().get_next_location_url()

    def get_first_incomplete_repeating_block_url(self, list_item_id):
        if first_incomplete_block := self.get_first_incomplete_repeating_block_location_for_list_item(
            repeating_block_ids=self.repeating_block_ids,
            section_id=self.current_location.section_id,
            list_item_id=list_item_id,
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

        return None

    def handle_post(self):
        self.questionnaire_store_updater.add_completed_location(self.current_location)
        if not self.get_first_incomplete_repeating_block_location_for_list_item(
            repeating_block_ids=self.repeating_block_ids,
            section_id=self.current_location.section_id,
            list_item_id=self.current_location.list_item_id,
            list_name=self.current_location.list_name,
        ):
            self.questionnaire_store_updater.update_section_or_repeating_blocks_progress_completion_status(
                is_complete=True,
                section_id=self.current_location.section_id,
                list_item_id=self.current_location.list_item_id,
            )

        # Cannot invoke parent handle_post as that would invoke self.update_section_completeness which overwrites the progress update done here
        self.questionnaire_store_updater.update_answers(self.form.data)
        if self.questionnaire_store_updater.is_dirty():
            self._routing_path = self.router.routing_path(
                self.current_location.section_id, self.current_location.list_item_id
            )
            self.questionnaire_store_updater.remove_dependent_blocks_and_capture_dependent_sections()
            self.questionnaire_store_updater.update_progress_for_dependent_sections()
            self.questionnaire_store_updater.save()
