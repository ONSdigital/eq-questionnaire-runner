from functools import partial

from flask import url_for
from flask_babel import lazy_gettext

from app.views.contexts import Context


class ListContext(Context):
    def __call__(self, list_collector_block, return_to=None, editable=True):
        if "summary" not in list_collector_block:
            return None

        return {
            "list": {
                "list_items": list(
                    self._build_list_items_summary_context(
                        list_collector_block, return_to=return_to
                    )
                ),
                "editable": editable,
            }
        }

    def _build_list_items_summary_context(
        self, list_collector_block, return_to, editable=True
    ):
        list_name = list_collector_block["for_list"]
        list_item_ids = self._list_store[list_name].items
        primary_person = self._list_store[list_name].primary_person

        for list_item_id in list_item_ids:
            partial_url_for = partial(
                url_for,
                "questionnaire.block",
                list_name=list_name,
                list_item_id=list_item_id,
                return_to=return_to,
            )

            is_primary = list_item_id == primary_person
            list_item_context = {}

            list_item_context = {
                "item_title": self._get_item_title(
                    list_collector_block["summary"], list_item_id, is_primary
                ),
                "primary_person": is_primary,
            }

            if editable:
                if "edit_block" in list_collector_block:
                    list_item_context["edit_link"] = partial_url_for(
                        block_id=list_collector_block["edit_block"]["id"]
                    )

                if "remove_block" in list_collector_block:
                    list_item_context["remove_link"] = partial_url_for(
                        block_id=list_collector_block["remove_block"]["id"]
                    )

            yield list_item_context

    def _get_item_title(self, list_block_summary, list_item_id, is_primary):
        rendered_summary = self._placeholder_renderer.render(
            list_block_summary, list_item_id
        )

        if is_primary:
            rendered_summary["item_title"] += lazy_gettext(" (You)")

        return rendered_summary["item_title"]
