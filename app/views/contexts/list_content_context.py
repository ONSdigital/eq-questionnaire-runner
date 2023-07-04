from typing import Any, Generator, Mapping, Optional

from werkzeug.datastructures import ImmutableDict

from app.views.contexts.context import Context


class ListContentContext(Context):
    def __call__(
        self,
        summary_definition: Mapping[str, Any],
        content_definition: ImmutableDict,
        for_list: str,
        section_id: str,
        has_repeating_blocks: bool,
        return_to: Optional[str] = None,
    ) -> dict[str, Any]:
        list_items = (
            list(
                self._build_list_items_context(
                    for_list=for_list,
                    section_id=section_id,
                    has_repeating_blocks=has_repeating_blocks,
                    summary_definition=summary_definition,
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
        *,
        for_list: str,
        section_id: str,
        has_repeating_blocks: bool,
        summary_definition: Mapping,
    ) -> Generator[dict, None, None]:
        list_item_ids = self._list_store[for_list]

        for list_item_id in list_item_ids:
            yield {
                "item_title": self._get_item_title(summary_definition, list_item_id),
                "primary_person": False,
                "list_item_id": list_item_id,
                "is_complete": self._progress_store.is_section_or_repeating_blocks_progress_complete(
                    section_id=section_id, list_item_id=list_item_id
                ),
                "repeating_blocks": has_repeating_blocks,
            }

    def _get_item_title(
        self, summary_definition: Mapping[str, Any], list_item_id: Optional[str]
    ) -> str:
        rendered_summary: dict[str, Any] = self._placeholder_renderer.render(
            data_to_render=summary_definition, list_item_id=list_item_id
        )

        title: str = rendered_summary["item_title"]
        return title
