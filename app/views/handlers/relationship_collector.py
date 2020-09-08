from functools import cached_property

from app.data_models.relationship_store import RelationshipStore
from app.questionnaire.location import Location
from app.questionnaire.relationship_router import RelationshipRouter
from app.views.handlers.question import Question


class RelationshipCollector(Question):
    @cached_property
    def relationship_router(self):
        block_id = self._current_location.block_id
        section_id = self._current_location.section_id
        list_items = self._questionnaire_store.list_store[
            self._schema.get_block(block_id)["for_list"]
        ].items
        return RelationshipRouter(
            section_id=section_id, block_id=block_id, list_item_ids=list_items
        )

    @property
    def parent_location(self):
        return Location(
            section_id=self._current_location.section_id, block_id=self.block["id"]
        )

    def _get_routing_path(self):
        return self.router.routing_path(section_id=self.parent_location.section_id)

    def is_location_valid(self):
        if isinstance(self._current_location, Location):
            return self.router.can_access_location(
                self._current_location, self._routing_path
            )

        can_access_parent_location = self.router.can_access_location(
            self.parent_location, self._routing_path
        )
        can_access_relationship_location = self.relationship_router.can_access_location(
            self._current_location
        )
        if not can_access_parent_location or not can_access_relationship_location:
            return False
        return True

    def get_first_location_url(self):
        if self.resume:
            return self.relationship_router.get_first_location_url(self.resume)
        return self.relationship_router.get_first_location_url()

    def get_previous_location_url(self):
        previous_location_url = self.relationship_router.get_previous_location_url(
            self._current_location
        )
        if not previous_location_url:
            previous_location_url = self.router.get_previous_location_url(
                self.parent_location, self._routing_path
            )
        return previous_location_url

    def get_next_location_url(self):
        next_location_url = self.relationship_router.get_next_location_url(
            self._current_location
        )
        if next_location_url:
            return next_location_url

        return self.router.get_next_location_url(
            self.parent_location, self._routing_path, self._return_to
        )

    def handle_post(self):
        self.questionnaire_store_updater.update_relationship_answer(
            self.form.data,
            self._current_location.list_item_id,
            self._current_location.to_list_item_id,
        )

        if self._is_last_relationship():
            self.questionnaire_store_updater.add_completed_location(
                location=self.parent_location
            )
            self._update_section_completeness(location=self.parent_location)

        self.questionnaire_store_updater.save()

    def _get_answers_from_answer_store(self, answer_ids):
        """
        Maps the answers in an answer store to a dictionary of key, value answers.
        """
        answer = self._questionnaire_store.answer_store.get_answer(answer_ids[0])
        if answer:
            relationship_store = RelationshipStore(answer.value)
            relationship = relationship_store.get_relationship(
                self._current_location.list_item_id,
                self._current_location.to_list_item_id,
            )
            if relationship:
                return {answer.answer_id: relationship.relationship}
        return {}

    def _is_last_relationship(self):
        if self.relationship_router.get_next_location_url(self._current_location):
            return False
        return True
