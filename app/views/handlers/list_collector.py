from typing import Generator

from flask import url_for

from app.views.contexts import ListContext
from app.views.handlers.question import Question


class ListCollector(Question):
    def __init__(self, *args):
        self._is_adding = False
        super().__init__(*args)

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

        if not self._is_list_collector_complete() and (incomplete_block := next(self._get_incomplete_repeating_block_ids(), None)):
            repeating_block_url = url_for(
                "questionnaire.block",
                list_name=self.rendered_block["for_list"],
                list_item_id=incomplete_block[0],
                block_id=incomplete_block[1],
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
                for_list=self.rendered_block["for_list"],
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
        elif not self.rendered_block["repeating_blocks"] or (self.rendered_block["repeating_blocks"] and self._is_list_collector_complete()):
            return super().handle_post()

    def _is_list_collector_complete(self):
        list_model = self._questionnaire_store.list_store.get(self.rendered_block["for_list"])
        return all(
            self.questionnaire_store_updater.is_section_complete(section_id=self.current_location.section_id, list_item_id=list_item_id)
            for list_item_id in list_model.items)

    def _get_incomplete_repeating_block_ids(self) -> Generator:
        list_model = self._questionnaire_store.list_store.get(self.rendered_block["for_list"])
        repeating_blocks = self.rendered_block.get("repeating_blocks")

        for list_item_id in list_model.items:
            if not self.questionnaire_store_updater.is_section_complete(self.current_location.section_id, list_item_id):
                complete_block_ids = self.questionnaire_store_updater.get_completed_block_ids(self.current_location.section_id, list_item_id)
                for repeating_block in repeating_blocks:
                    if repeating_block["id"] not in complete_block_ids:
                        yield list_item_id, repeating_block["id"]
