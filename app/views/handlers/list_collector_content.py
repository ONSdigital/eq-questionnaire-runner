from functools import cached_property

from flask import url_for

from app.views.contexts import ListContext
from app.views.handlers.question import Question


class ListCollectorContent(Question):
    @cached_property
    def repeating_block_ids(self) -> list[str]:
        return [
            block["id"] for block in self.rendered_block.get("repeating_blocks", [])
        ]

    @cached_property
    def list_name(self) -> str:
        return self.rendered_block["for_list"]

    def get_context(self):
        list_context = ListContext(
            self._language,
            self._schema,
            self._questionnaire_store.answer_store,
            self._questionnaire_store.list_store,
            self._questionnaire_store.progress_store,
            self._questionnaire_store.metadata,
            self._questionnaire_store.response_metadata,
        )

        return {
            **list_context(
                summary_definition=self.rendered_block["summary"],
                content_definition=self.rendered_block["content"],
                section_id=self.current_location.section_id,
                for_list=self.rendered_block["for_list"],
                return_to=self._return_to,
                has_repeating_blocks=bool(self.repeating_block_ids),
            ),
        }

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
        list_name = self._schema.get_repeating_blocks_list_for_section(
            self.current_location.section_id
        )
        return not self.get_first_incomplete_repeating_block_location(
            repeating_block_ids=self.repeating_block_ids,
            section_id=self.current_location.section_id,
            list_name=list_name,
        )
