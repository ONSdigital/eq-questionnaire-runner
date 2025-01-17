from functools import cached_property

from werkzeug.datastructures import ImmutableDict

from app.questionnaire.variants import transform_variants
from app.views.handlers.block import BlockHandler


class Content(BlockHandler):
    @cached_property
    def rendered_block(self) -> dict:
        transformed_block = transform_variants(
            self.block,
            self._schema,
            self._questionnaire_store.data_stores,
            self._current_location,
        )

        content_page_title = transformed_block.get(
            "page_title"
        ) or self._get_content_title(transformed_block)
        self._set_page_title(content_page_title)
        return self.placeholder_renderer.render(
            data_to_render=transformed_block,
            list_item_id=self._current_location.list_item_id,
        )

    def get_context(self) -> dict:
        return {"block": self.rendered_block}

    def _get_content_title(self, transformed_block: ImmutableDict) -> str | None:
        content = transformed_block.get("content")
        if content:
            return self._get_safe_page_title(content["title"])
