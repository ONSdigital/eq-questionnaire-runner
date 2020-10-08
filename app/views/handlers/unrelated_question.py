from app.questionnaire.location import Location
from app.views.handlers.question import Question


class UnrelatedQuestion(Question):
    @property
    def parent_location(self):
        parent_block_id = self._schema.parent_id_map[self.block["id"]]
        return Location(
            section_id=self._current_location.section_id, block_id=parent_block_id
        )

    def _get_routing_path(self):
        return self.router.routing_path(section_id=self.parent_location.section_id)

    def is_location_valid(self):
        can_access_parent_location = self.router.can_access_location(
            self.parent_location, self._routing_path
        )

        if not self.router.is_list_item_in_list_store(
            self.current_location.list_item_id, self.current_location.list_name
        ):
            return False

        return can_access_parent_location

    def get_previous_location_url(self):
        pass

    def get_next_location_url(self):
        pass  # pragma: no cover

    def handle_post(self):
        pass  # pragma: no cover
