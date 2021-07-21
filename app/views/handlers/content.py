from functools import cached_property

from app.questionnaire.schema_utils import transform_variants
from app.views.handlers import individual_response_url
from app.views.handlers.block import BlockHandler


class Content(BlockHandler):
    @cached_property
    def rendered_block(self):
        transformed_block = transform_variants(
            self.block,
            self._schema,
            self._questionnaire_store.metadata,
            self._questionnaire_store.answer_store,
            self._questionnaire_store.list_store,
            self._current_location,
        )

        content_page_title = transformed_block.get(
            "page_title"
        ) or self._get_content_title(transformed_block)
        self._set_page_title(content_page_title)
        return self.placeholder_renderer.render(
            transformed_block, self._current_location.list_item_id
        )

    def get_context(self):
        return {
            "block": self.rendered_block,
            "metadata": dict(self._questionnaire_store.metadata),
            "individual_response_url": individual_response_url(
                self._schema.get_individual_response_list(),
                self._current_location.list_item_id,
                self._questionnaire_store,
            )
            if self._is_block_first_block_in_individual_response()
            else None,
        }

    def _get_content_title(self, transformed_block):
        content = transformed_block.get("content")
        if content:
            return self._get_safe_page_title(content["title"])

    def _is_block_first_block_in_individual_response(self):
        individual_section_id = (
            self._schema.get_individual_response_individual_section_id()
        )
        return (
            self._current_location.section_id == individual_section_id
            and self._current_location.block_id == self._routing_path[0]
        )
