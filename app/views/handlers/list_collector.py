from functools import cached_property
from typing import Any

from flask import url_for

from app.views.contexts import ListContext
from app.views.handlers.question import Question


class ListCollector(Question):
    def __init__(self, *args: Any) -> None:
        self._is_adding = False
        super().__init__(*args)

    @cached_property
    def repeating_block_ids(self) -> list[str]:
        return [
            block["id"] for block in self.rendered_block.get("repeating_blocks", [])
        ]

    @cached_property
    def list_name(self) -> str:
        return self.rendered_block["for_list"]  # type: ignore

    def get_next_location_url(self) -> str:
        if self._is_adding:
            add_url = url_for(
                "questionnaire.block",
                list_name=self.rendered_block["for_list"],
                block_id=self.rendered_block["add_block"]["id"],
                **self.return_location.to_dict(),
            )
            return add_url

        if incomplete_block := self.get_first_incomplete_list_repeating_block_location(
            repeating_block_ids=self.repeating_block_ids,
            section_id=self.current_location.section_id,
            list_name=self.list_name,
        ):
            repeating_block_url = url_for(
                "questionnaire.block",
                list_name=self.list_name,
                list_item_id=incomplete_block.list_item_id,
                block_id=incomplete_block.block_id,
                **self.return_location.to_dict(),
            )
            return repeating_block_url

        return super().get_next_location_url()

    def _get_list_context(self) -> dict[str, dict]:
        list_context = ListContext(
            self._language,
            self._schema,
            self._questionnaire_store.data_stores,
        )

        return list_context(
            self.rendered_block["summary"],
            for_list=self.list_name,
            edit_block_id=self.rendered_block.get("edit_block", {}).get("id"),
            remove_block_id=self.rendered_block.get("remove_block", {}).get("id"),
            return_to=self.return_location.return_to,
            section_id=self.current_location.section_id,
            has_repeating_blocks=bool(self.repeating_block_ids),
        )

    def _get_additional_view_context(self) -> dict:
        """This is only needed so we can use it in List Collector Content class where we override the default behaviour of the Question class"""
        return super().get_context()

    def get_context(self) -> dict:
        return {**self._get_additional_view_context(), **self._get_list_context()}

    def handle_post(self) -> None:
        answer_action = self._get_answer_action()

        if answer_action and answer_action["type"] == "RedirectToListAddBlock":
            self._is_adding = True
            self.questionnaire_store_updater.update_answers(self.form.data)
            self.questionnaire_store_updater.save()
        elif self._is_list_collector_complete():
            super().handle_post()

    def _is_list_collector_complete(self) -> bool:
        return not self.get_first_incomplete_list_repeating_block_location(
            repeating_block_ids=self.repeating_block_ids,
            section_id=self.current_location.section_id,
            list_name=self.list_name,
        )
