from flask import url_for

from app.views.handlers.list_collector import ListCollector


class ListCollectorContent(ListCollector):
    def _get_additional_view_context(self) -> dict:
        return self.rendered_block["content"]

    def get_next_location_url(self):
        if incomplete_block := self.get_first_incomplete_repeating_block_location(
            repeating_block_ids=self.repeating_block_ids,
            section_id=self.current_location.section_id,
            list_name=self.list_name,
        ):
            return url_for(
                "questionnaire.block",
                list_name=self.list_name,
                list_item_id=incomplete_block.list_item_id,
                block_id=incomplete_block.block_id,
                return_to=self._return_to,
                return_to_answer_id=self._return_to_answer_id,
                return_to_block_id=self._return_to_block_id,
            )

        return self.router.get_next_location_url(
            self._current_location,
            self._routing_path,
            self._return_to,
            self._return_to_answer_id,
            self._return_to_block_id,
        )

    def handle_post(self):
        self._set_started_at_metadata()
        self.questionnaire_store_updater.add_completed_location()
        if self._is_list_collector_content_complete():
            self._update_section_completeness()
        self.questionnaire_store_updater.update_progress_for_dependent_sections()
        self.questionnaire_store_updater.save()

    def _is_list_collector_content_complete(self):
        list_name = self._schema.get_repeating_blocks_list_name_for_section(
            self.current_location.section_id
        )
        return not self.get_first_incomplete_repeating_block_location(
            repeating_block_ids=self.repeating_block_ids,
            section_id=self.current_location.section_id,
            list_name=list_name,
        )
