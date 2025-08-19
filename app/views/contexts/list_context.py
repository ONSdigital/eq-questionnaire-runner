from functools import partial
from typing import Any, Generator, Mapping, Sequence

from flask import url_for
from flask_babel import lazy_gettext

from app.questionnaire.location import SectionKey
from app.views.contexts.context import Context


class ListContext(Context):
    def __call__(
        self,
        summary_definition: Mapping,
        for_list: str,
        section_id: str,
        has_repeating_blocks: bool,
        return_to: str | None = None,
        edit_block_id: str | None = None,
        remove_block_id: str | None = None,
        primary_person_edit_block_id: str | None = None,
        for_list_item_ids: Sequence[str] | None = None,
    ) -> dict[str, Any]:
        list_items = (
            list(
                self._build_list_items_context(
                    for_list=for_list,
                    section_id=section_id,
                    has_repeating_blocks=has_repeating_blocks,
                    return_to=return_to,
                    summary_definition=summary_definition,
                    edit_block_id=edit_block_id,
                    remove_block_id=remove_block_id,
                    primary_person_edit_block_id=primary_person_edit_block_id,
                    for_list_item_ids=for_list_item_ids,
                )
            )
            if summary_definition
            else []
        )

        return {
            "list": {
                "list_items": list_items,
                "editable": any([edit_block_id, remove_block_id]),
            },
        }

    # pylint: disable=too-many-locals
    def _build_list_items_context(
        self,
        *,
        for_list: str,
        section_id: str,
        has_repeating_blocks: bool,
        return_to: str | None,
        summary_definition: Mapping,
        edit_block_id: str | None,
        remove_block_id: str | None,
        primary_person_edit_block_id: str | None,
        for_list_item_ids: Sequence[str] | None,
    ) -> Generator[dict]:
        list_item_ids = self._data_stores.list_store[for_list]
        if for_list_item_ids:
            list_item_ids = [
                list_item_id  # type: ignore
                for list_item_id in list_item_ids
                if list_item_id in for_list_item_ids
            ]
        primary_person = self._data_stores.list_store[for_list].primary_person

        for list_item_id in list_item_ids:
            partial_url_for = partial(
                url_for,
                "questionnaire.block",
                list_name=for_list,
                list_item_id=list_item_id,
                return_to=return_to,
            )

            is_primary = list_item_id == primary_person

            list_item_context = {
                "item_title": self._get_item_title(
                    summary_definition, list_item_id, is_primary
                ),
                "primary_person": is_primary,
                "list_item_id": list_item_id,
                "is_complete": self._data_stores.progress_store.is_section_complete(
                    SectionKey(section_id, list_item_id)
                ),
                "repeating_blocks": has_repeating_blocks,
            }

            if edit_block_id:
                block_id = (
                    primary_person_edit_block_id
                    if is_primary and primary_person_edit_block_id
                    else edit_block_id
                )
                # return to answer id is used to snap back to the appropriate list item when editing from a summary page
                # unlike other repeating answers that use answer_id-list_item_id, the edit-block is linked to item-label and anchored by list item id
                return_to_answer_id = list_item_id if return_to else None
                list_item_context["edit_link"] = partial_url_for(
                    block_id=block_id, return_to_answer_id=return_to_answer_id
                )

            if remove_block_id:
                list_item_context["remove_link"] = partial_url_for(
                    block_id=remove_block_id
                )

            yield list_item_context

    def _get_item_title(
        self,
        summary_definition: Mapping[str, Any],
        list_item_id: str | None,
        is_primary: bool,
    ) -> str:
        rendered_summary: dict[str, Any] = self._placeholder_renderer.render(
            data_to_render=summary_definition, list_item_id=list_item_id
        )
        if is_primary:
            rendered_summary["item_title"] += lazy_gettext(" (You)")

        title: str = rendered_summary["item_title"]
        return title
