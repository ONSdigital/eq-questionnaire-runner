from app.questionnaire.location import Location
from app.views.handlers.question import Question


class PrimaryPersonQuestion(Question):
    @property
    def parent_block(self):
        parent_block_id = self._schema.parent_id_map[self.rendered_block["id"]]
        return self._schema.get_block(parent_block_id)

    @property
    def parent_location(self):
        parent_id = self._schema.parent_id_map[self.rendered_block["id"]]
        return Location(
            section_id=self._current_location.section_id, block_id=parent_id
        )

    def _get_routing_path(self):
        return self.router.routing_path(section_id=self._current_location.section_id)

    def is_location_valid(self):
        primary_person_list_item_id = self._questionnaire_store.list_store[
            self.current_location.list_name
        ].primary_person

        return (
            self.current_location.list_item_id == primary_person_list_item_id
            and self.router.can_access_location(
                self.parent_location, self._routing_path
            )
        )

    def get_previous_location_url(self):
        return self.parent_location.url()

    def get_next_location_url(self):
        return self.router.get_next_location_url(
            self.parent_location, self._routing_path, self._return_to
        )

    def handle_post(self):
        same_name_answer_ids = self.parent_block.get("same_name_answer_ids")
        self.questionnaire_store_updater.update_answers(self.form.data)
        self.questionnaire_store_updater.update_same_name_items(
            self.parent_block["for_list"], same_name_answer_ids
        )

        self.questionnaire_store_updater.add_completed_location(
            location=self.parent_location
        )

        self._update_section_completeness(location=self.parent_location)
        self.questionnaire_store_updater.save()
