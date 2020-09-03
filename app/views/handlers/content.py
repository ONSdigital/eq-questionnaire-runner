from functools import cached_property

from app.questionnaire.schema_utils import transform_variants
from app.views.handlers import individual_response_url
from app.views.handlers.block import BlockHandler


class Content(BlockHandler):
    @cached_property
    def rendered_block(self):
        return self._render_block(self.block["id"])

    def get_context(self):
        return {
            "block": self.rendered_block,
            "metadata": dict(self._questionnaire_store.metadata),
            "individual_response_url": individual_response_url(
                self._schema.get_individual_response_list(),
                self._current_location.list_item_id,
                self._questionnaire_store,
            ),
        }

    def _render_block(self, block_id):
        block_schema = self._schema.get_block(block_id)
        transformed_block = transform_variants(
            block_schema,
            self._schema,
            self._questionnaire_store.metadata,
            self._questionnaire_store.answer_store,
            self._questionnaire_store.list_store,
            self._current_location,
        )

        self.page_title = self._get_page_title(transformed_block)

        return self.placeholder_renderer.render(
            transformed_block, self._current_location.list_item_id
        )

    def _get_page_title(self, transformed_block):
        content = transformed_block.get("content")
        if content:
            return self._get_safe_page_title(content["title"])
