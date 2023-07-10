from typing import Any

from flask import url_for

from app.views.contexts import ListContext
from app.views.handlers.question import Question


class ListCollector(Question):
    def __init__(self, *args: Any) -> None:
        self._is_adding = False
        super().__init__(*args)

    def get_next_location_url(self) -> str:
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

        return super().get_next_location_url()

    def get_context(self) -> dict[str, dict]:
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

    def handle_post(self) -> None:
        answer_action = self._get_answer_action()

        if answer_action and answer_action["type"] == "RedirectToListAddBlock":
            self._is_adding = True
            # pylint: disable=no-member
            # wtforms Form parents are not discoverable in the 2.3.3 implementation
            self.questionnaire_store_updater.update_answers(self.form.data)
            self.questionnaire_store_updater.save()
        else:
            super().handle_post()
