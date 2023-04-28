from enum import Enum
from typing import Any

from flask import url_for

from app.views.contexts import ListContext
from app.views.handlers.question import Question


class ListCollectorAddType(Enum):
    SINGLE = "RedirectToListAddBlock"
    MULTI = "RedirectToListRepeatingBlocks"


class ListCollector(Question):
    def __init__(self, *args: Any):
        self._add_type: ListCollectorAddType | None = None
        super().__init__(*args)

    def get_next_location_url(self):
        if self._add_type == ListCollectorAddType.SINGLE:
            add_url = url_for(
                "questionnaire.block",
                list_name=self.rendered_block["for_list"],
                block_id=self.rendered_block["add_block"]["id"],
                return_to=self._return_to,
                return_to_answer_id=self._return_to_answer_id,
                return_to_block_id=self._return_to_block_id,
            )
            return add_url

        if self._add_type == ListCollectorAddType.MULTI:
            repeating_block_url = url_for(
                "questionnaire.block",
                list_name=self.rendered_block["for_list"],
                block_id=self.rendered_block["repeating_blocks"][0]["id"],
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
        if answer_action := self._get_answer_action():
            if answer_action["type"] in set(add_type.value for add_type in ListCollectorAddType):
                self._add_type = ListCollectorAddType(answer_action["type"])

        if self._add_type:
            # pylint: disable=no-member
            # wtforms Form parents are not discoverable in the 2.3.3 implementation
            self.questionnaire_store_updater.update_answers(self.form.data)
            self.questionnaire_store_updater.save()
        else:
            return super().handle_post()
