from functools import cached_property

from flask import url_for

from app.views.contexts import ListContext
from app.views.handlers.question import Question


class ListCollector(Question):
    def __init__(self, *args):
        self._is_adding = False
        super().__init__(*args)

    @cached_property
    def repeating_block_ids(self) -> list[str]:
        return [block["id"] for block in self.rendered_block.get("repeating_blocks", [])]

    @cached_property
    def list_name(self) -> str:
        return self.rendered_block.get("for_list")

    def get_next_location_url(self):
        if self._is_adding:
            add_url = url_for(
                "questionnaire.block",
                list_name=self.rendered_block["for_list"],
                block_id=self.rendered_block["add_block"]["id"],
                return_to=self._return_to,
                return_to_answer_id=self._return_to_answer_id,
                return_to_block_id=self._return_to_block_id,
            )
            return add_url

        if incomplete_block := self.get_first_incomplete_repeating_block_location(self.repeating_block_ids, self.current_location.section_id, self.list_name):
            repeating_block_url = url_for(
                "questionnaire.block",
                list_name=self.list_name,
                list_item_id=incomplete_block.list_item_id,
                block_id=incomplete_block.block_id,
                return_to=self._return_to,
                return_to_answer_id=self._return_to_answer_id,
                return_to_block_id=self._return_to_block_id,
            )
            return repeating_block_url

        return super().get_next_location_url()

    def get_context(self):
        question_context = super().get_context()
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
            **question_context,
            **list_context(
                self.rendered_block["summary"],
                for_list=self.list_name,
                list_collector_location=self.current_location,
                edit_block_id=self.rendered_block["edit_block"]["id"],
                remove_block_id=self.rendered_block["remove_block"]["id"],
                return_to=self._return_to,
            ),
        }

    def handle_post(self):
        answer_action = self._get_answer_action()

        if answer_action and answer_action["type"] == "RedirectToListAddBlock":
            self._is_adding = True
            # pylint: disable=no-member
            # wtforms Form parents are not discoverable in the 2.3.3 implementation
            self.questionnaire_store_updater.update_answers(self.form.data)
            self.questionnaire_store_updater.save()
        elif self._is_list_collector_complete():
            return super().handle_post()

    def _is_list_collector_complete(self):
        return not self.get_first_incomplete_repeating_block_location(repeating_block_ids=self.repeating_block_ids,
                                                                      section_id=self.current_location.section_id,
                                                                      list_name=self.list_name)
