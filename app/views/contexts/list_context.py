from functools import partial

from flask import url_for
from flask_babel import lazy_gettext

from . import Context


class ListContext(Context):
    def __call__(
        self,
        summary_definition,
        for_list,
        return_to_summary=None,
        edit_block_id=None,
        remove_block_id=None,
    ):
        list_items = (
            list(
                self._build_list_items_context(
                    for_list,
                    return_to_summary,
                    summary_definition,
                    edit_block_id,
                    remove_block_id,
                )
            )
            if summary_definition
            else []
        )

        return {
            "list": {
                "list_items": list_items,
                "editable": any([edit_block_id, remove_block_id]),
            }
        }

    def _build_list_items_context(
        self,
        for_list,
        return_to_summary,
        summary_definition,
        edit_block_id,
        remove_block_id,
    ):
        list_item_ids = self._list_store[for_list].items
        primary_person = self._list_store[for_list].primary_person

        for list_item_id in list_item_ids:
            partial_url_for = partial(
                url_for,
                "questionnaire.block",
                list_name=for_list,
                list_item_id=list_item_id,
                return_to_summary=return_to_summary,
            )

            is_primary = list_item_id == primary_person

            list_item_context = {
                "item_title": self._get_item_title(
                    summary_definition, list_item_id, is_primary
                ),
                "primary_person": is_primary,
            }

            if edit_block_id:
                list_item_context["edit_link"] = partial_url_for(block_id=edit_block_id)

            if remove_block_id:
                list_item_context["remove_link"] = partial_url_for(
                    block_id=remove_block_id
                )

            yield list_item_context

    def _get_item_title(self, summary_definition, list_item_id, is_primary):
        rendered_summary = self._placeholder_renderer.render(
            summary_definition, list_item_id
        )

        if is_primary:
            rendered_summary["item_title"] += lazy_gettext(" (You)")

        return rendered_summary["item_title"]
