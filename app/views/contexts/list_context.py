from functools import partial

from flask import url_for
from flask_babel import lazy_gettext

from . import Context


class ListContext(Context):
    def __init__(
        self,
        language,
        schema,
        answer_store,
        list_store,
        progress_store,
        metadata,
        summary_definition,
        for_list,
        return_to=None,
        edit_block_id=None,
        remove_block_id=None,
    ):
        super().__init__(
            language, schema, answer_store, list_store, progress_store, metadata
        )

        self._summary_definition = summary_definition
        self._for_list = for_list
        self._return_to = return_to
        self._edit_block_id = edit_block_id
        self._remove_block_id = remove_block_id
        self._editable = self._edit_block_id or self._remove_block_id

        list_items = (
            list(self._build_list_items_context()) if summary_definition else []
        )

        self._context = {
            "list": {
                "list_items": list_items,
                "editable": any([edit_block_id, remove_block_id]),
            }
        }

    def get_context(self):
        return self._context

    def _build_list_items_context(self):
        list_item_ids = self._list_store[self._for_list].items
        primary_person = self._list_store[self._for_list].primary_person

        for list_item_id in list_item_ids:
            partial_url_for = partial(
                url_for,
                "questionnaire.block",
                list_name=self._for_list,
                list_item_id=list_item_id,
                return_to=self._return_to,
            )

            is_primary = list_item_id == primary_person

            list_item_context = {
                "item_title": self._get_item_title(list_item_id, is_primary),
                "primary_person": is_primary,
            }

            if self._editable:
                if self._edit_block_id:
                    list_item_context["edit_link"] = partial_url_for(
                        block_id=self._edit_block_id
                    )

                if self._remove_block_id:
                    list_item_context["remove_link"] = partial_url_for(
                        block_id=self._remove_block_id
                    )

            yield list_item_context

    def _get_item_title(self, list_item_id, is_primary):
        rendered_summary = self._placeholder_renderer.render(
            self._summary_definition, list_item_id
        )

        if is_primary:
            rendered_summary["item_title"] += lazy_gettext(" (You)")

        return rendered_summary["item_title"]
