from functools import partial

from flask import url_for
from flask_babel import lazy_gettext

from . import Context


class ListContext(Context):
    def __call__(
        self,
        summary_definition,
        for_list,
        return_to=None,
        editable=True,
        edit_block=None,
        remove_block=None,
    ):
        list_items = list(
            self._build_list_items_summary_context(
                summary_definition,
                for_list,
                return_to=return_to,
                edit_block=edit_block,
                remove_block=remove_block,
            )
        )
        return {"list": {"list_items": list_items, "editable": editable}}

    def _build_list_items_summary_context(
        self,
        summary_definition,
        for_list,
        return_to,
        editable=True,
        edit_block=None,
        remove_block=None,
    ):
        if not summary_definition:
            return None

        list_item_ids = self._list_store[for_list].items
        primary_person = self._list_store[for_list].primary_person

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
            }

            if editable:
                if edit_block:
                    list_item_context["edit_link"] = partial_url_for(
                        block_id=edit_block["id"]
                    )

                if remove_block:
                    list_item_context["remove_link"] = partial_url_for(
                        block_id=remove_block["id"]
                    )

            yield list_item_context

    def _get_item_title(self, summary_definition, list_item_id, is_primary):
        rendered_summary = self._placeholder_renderer.render(
            summary_definition, list_item_id
        )

        if is_primary:
            rendered_summary["item_title"] += lazy_gettext(" (You)")

        return rendered_summary["item_title"]
