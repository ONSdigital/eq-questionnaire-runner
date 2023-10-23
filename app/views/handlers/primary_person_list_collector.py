from typing import Any

from flask import url_for

from app.views.handlers.question import Question


class PrimaryPersonListCollector(Question):
    def __init__(self, *args: Any):
        self._is_adding = False
        self._primary_person_id: str | None = None
        super().__init__(*args)

    def get_next_location_url(self) -> str:
        if self._is_adding:
            add_or_edit_url = url_for(
                "questionnaire.block",
                list_name=self.rendered_block["for_list"],
                block_id=self.rendered_block["add_or_edit_block"]["id"],
                list_item_id=self._primary_person_id,
            )
            return add_or_edit_url

        return super().get_next_location_url()

    def handle_post(self) -> None:
        list_name = self.rendered_block["for_list"]
        answer_action = self._get_answer_action()

        if answer_action and answer_action["type"] == "RedirectToListAddBlock":
            self._is_adding = True
            # pylint: disable=no-member
            # wtforms Form parents are not discoverable in the 2.3.3 implementation
            self.questionnaire_store_updater.update_answers(self.form.data)
            self._primary_person_id = (
                self.questionnaire_store_updater.add_primary_person(list_name)
            )
            self.questionnaire_store_updater.remove_dependent_blocks_and_capture_dependent_sections()
            self.questionnaire_store_updater.update_progress_for_dependent_sections()
            self.questionnaire_store_updater.save()
        else:
            # This method could determine the current section's status incorrectly, as
            # the call to update the answer store takes place in
            # `super().handle_post()`. The section status will eventually get
            # determined correctly when the parent class' `update_section_status`
            # method is called.
            self.questionnaire_store_updater.remove_primary_person(list_name)
            self.questionnaire_store_updater.update_same_name_items(
                list_name, self.rendered_block.get("same_name_answer_ids")
            )
            super().handle_post()
