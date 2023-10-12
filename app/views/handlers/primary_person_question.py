from werkzeug.datastructures import ImmutableDict

from app.questionnaire.location import Location
from app.questionnaire.routing_path import RoutingPath
from app.views.handlers.question import Question


class PrimaryPersonQuestion(Question):
    @property
    def parent_block(self) -> ImmutableDict:
        parent_block_id = self._schema.parent_id_map[self.rendered_block["id"]]
        # Type ignore: being called with a valid block_id
        return self._schema.get_block(parent_block_id)  # type: ignore

    @property
    def parent_location(self) -> Location:
        parent_id = self._schema.parent_id_map[self.block["id"]]
        return Location(
            section_id=self._current_location.section_id, block_id=parent_id
        )

    def _get_routing_path(self) -> RoutingPath:
        return self.router.routing_path(self.parent_location.section_key)

    def is_location_valid(self) -> bool:
        primary_person_list_item_id = self._questionnaire_store.list_store[
            # Type ignore: list_name will exist by this point
            self.current_location.list_name  # type: ignore
        ].primary_person

        return (
            self.current_location.list_item_id == primary_person_list_item_id
            and self.router.can_access_location(
                self.parent_location, self._routing_path
            )
        )

    def get_previous_location_url(self) -> str:
        return self.parent_location.url()

    def get_next_location_url(self) -> str:
        return self.router.get_next_location_url(
            self.parent_location, self._routing_path, self._return_location
        )

    def handle_post(self) -> None:
        same_name_answer_ids = self.parent_block.get("same_name_answer_ids")
        # pylint: disable=no-member
        # wtforms Form parents are not discoverable in the 2.3.3 implementation
        self.questionnaire_store_updater.update_answers(self.form.data)
        self.questionnaire_store_updater.update_same_name_items(
            self.parent_block["for_list"], same_name_answer_ids
        )

        self.questionnaire_store_updater.add_completed_location(
            location=self.parent_location
        )

        self.questionnaire_store_updater.remove_dependent_blocks_and_capture_dependent_sections()
        self._update_section_completeness(location=self.parent_location)
        self.questionnaire_store_updater.update_progress_for_dependent_sections()
        self.questionnaire_store_updater.save()
