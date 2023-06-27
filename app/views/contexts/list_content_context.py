from typing import Any, Generator, Mapping, Optional, Sequence

from flask_babel import lazy_gettext
from werkzeug.datastructures import ImmutableDict

from app.views.contexts.context import Context


class ListContentContext(Context):
    def __call__(
        self,
        summary_definition: Mapping[str, Any],
        content_definition: ImmutableDict,
        for_list: str,
        return_to: Optional[str] = None,
        for_list_item_ids: Optional[Sequence[str]] = None,
    ) -> dict[str, Any]:
        list_items = (
            list(
                self._build_list_items_context(
                    for_list,
                    summary_definition,
                    for_list_item_ids,
                )
            )
            if summary_definition
            else []
        )

        return {
            "list": {
                "list_items": list_items,
                "editable": False,
            },
            "content": content_definition,
        }

    def _build_list_items_context(
        self,
        for_list: str,
        summary_definition: Mapping[str, Any],
        for_list_item_ids: Optional[Sequence[str]],
    ) -> Generator[dict[str, Any], Any, None]:
        list_item_ids = self._list_store[for_list]
        if for_list_item_ids:
            list_item_ids = [
                list_item_id  # type: ignore
                for list_item_id in list_item_ids
                if list_item_id in for_list_item_ids
            ]

        for list_item_id in list_item_ids:
            yield {
                "item_title": self._get_item_title(
                    summary_definition, list_item_id, False
                ),
                "primary_person": False,
                "list_item_id": list_item_id,
            }

    def _get_item_title(
        self,
        summary_definition: Mapping[str, Any],
        list_item_id: Optional[str],
        is_primary: bool,
    ) -> str:
        rendered_summary: dict[str, Any] = self._placeholder_renderer.render(
            data_to_render=summary_definition, list_item_id=list_item_id
        )
        if is_primary:
            rendered_summary["item_title"] += lazy_gettext(" (You)")

        title: str = rendered_summary["item_title"]
        return title
