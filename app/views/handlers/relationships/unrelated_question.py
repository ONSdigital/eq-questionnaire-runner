from functools import cached_property

from app.questionnaire.location import Location
from app.views.handlers.question import Question


class UnrelatedQuestion(Question):
    @cached_property
    def list_name(self):
        parent_block_id = self._schema.parent_id_map[self.block["id"]]
        return self._schema.get_block(parent_block_id)["for_list"]

    @cached_property
    def parent_location(self):
        parent_block_id = self._schema.parent_id_map[self.block["id"]]
        return Location(
            section_id=self._current_location.section_id, block_id=parent_block_id
        )

    @cached_property
    def remaining_relationship_list_item_ids(self):
        list_model = self._questionnaire_store.list_store[self.list_name]
        start = list_model.index(self._current_location.list_item_id) + 1
        return list_model[start:]

    def get_list_summary_context(self):
        return self.list_context(
            self.rendered_block["list_summary"]["summary"],
            self.rendered_block["list_summary"]["for_list"],
            for_list_item_ids=self.remaining_relationship_list_item_ids,
        )

    def _get_routing_path(self):
        return self.router.routing_path(section_id=self.parent_location.section_id)

    def is_location_valid(self):
        can_access_parent_location = self.router.can_access_location(
            self.parent_location, self._routing_path
        )

        if not can_access_parent_location:
            return False

        if self.current_location.list_name != self.list_name or (
            self.current_location.list_item_id
            and not self.router.is_list_item_in_list_store(
                self.current_location.list_item_id, self.current_location.list_name
            )
        ):
            return False

        return True

    def get_previous_location_url(self):
        pass

    def get_next_location_url(self):
        pass  # pragma: no cover

    def handle_post(self):
        pass  # pragma: no cover
