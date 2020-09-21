from app.views.handlers import individual_response_url
from app.views.handlers.block import BlockHandler


class Content(BlockHandler):
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
