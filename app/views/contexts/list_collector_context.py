from flask import url_for
from flask_babel import lazy_gettext
from functools import partial

from app.views.contexts.context import Context
from app.views.contexts.question import build_question_context


class ListCollectorContext(Context):
    def get_item_title(self, list_block_summary, list_item_id, is_primary):
        rendered_summary = self._placeholder_renderer.render(
            list_block_summary, list_item_id
        )

        if is_primary:
            rendered_summary["item_title"] += lazy_gettext(" (You)")

        return rendered_summary["item_title"]

    def build_list_items_summary_context(self, list_collector_block, return_to=None):
        list_name = list_collector_block["for_list"]
        list_item_ids = self._list_store[list_name].items

        primary_person = self._list_store[list_name].primary_person

        list_items = []

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

            if "summary" in list_collector_block:
                list_item_context = {
                    "item_title": self.get_item_title(
                        list_collector_block["summary"], list_item_id, is_primary
                    ),
                    "primary_person": is_primary,
                }

                if "edit_block" in list_collector_block:
                    list_item_context["edit_link"] = partial_url_for(
                        block_id=list_collector_block["edit_block"]["id"]
                    )

                if "remove_block" in list_collector_block:
                    list_item_context["remove_link"] = partial_url_for(
                        block_id=list_collector_block["remove_block"]["id"]
                    )

            list_items.append(list_item_context)

        return list_items

    def build_list_collector_context(self, list_collector_block, form):
        question_context = build_question_context(list_collector_block, form)
        list_collector_context = {
            "list": {
                "list_items": self.build_list_items_summary_context(
                    list_collector_block
                ),
                "editable": True,
            }
        }

        return {**question_context, **list_collector_context}
