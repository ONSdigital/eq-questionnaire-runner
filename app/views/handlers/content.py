from functools import cached_property
from typing import Union

from flask import url_for

from app.questionnaire.schema_utils import transform_variants
from app.views.handlers.block import BlockHandler


class Content(BlockHandler):
    @cached_property
    def rendered_block(self):
        return self._render_block(self.block["id"])

    def get_context(self):
        return {
            "block": self.rendered_block,
            "metadata": dict(self._questionnaire_store.metadata),
            "individual_response_url": self._individual_response_url(),
        }

    def _individual_response_url(self) -> Union[str, None]:
        if "individual_response" in self._schema.json:
            for_list = self._schema.json["individual_response"]["for_list"]
            list_item_id = self._current_location.list_item_id

            primary_person_id = self._questionnaire_store.list_store[
                for_list
            ].primary_person

            if list_item_id != primary_person_id:
                return url_for(
                    "individual_response.request_individual_response",
                    list_item_id=list_item_id,
                )

        return None

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
