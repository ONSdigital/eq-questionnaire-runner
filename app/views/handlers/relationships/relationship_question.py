from functools import cached_property

from app.data_models.relationship_store import RelationshipStore
from app.questionnaire.location import Location
from app.questionnaire.relationship_router import RelationshipRouter
from app.views.handlers.question import Question


class RelationshipQuestion(Question):
    @cached_property
    def relationships_block(self):
        return self._schema.get_block(self.block["id"])

    @cached_property
    def relationships_answer_id(self):
        return self._schema.get_first_answer_id_for_block(
            self.relationships_block["id"]
        )

    @property
    def parent_location(self):
        return Location(
            section_id=self._current_location.section_id,
            block_id=self.relationships_block["id"],
        )

    @cached_property
    def unrelated_block_id(self):
        return self.relationships_block.get("unrelated_block", {}).get("id")

    @cached_property
    def unrelated_answer_id(self):
        if self.unrelated_block_id:
            return self._schema.get_first_answer_id_for_block(self.unrelated_block_id)
        return None

    @cached_property
    def unrelated_no_answer_values(self):
        if self.unrelated_answer_id:
            return self._schema.get_unrelated_block_no_answer_values(
                self.unrelated_answer_id
            )

    @cached_property
    def relationship_store(self):
        answer = self._questionnaire_store.answer_store.get_answer(
            self.relationships_answer_id
        )
        if answer:
            return RelationshipStore(answer.value)
        return RelationshipStore()

    @property
    def relationship_router(self):
        list_name = self.relationships_block["for_list"]
        list_items = self._questionnaire_store.list_store[list_name].items

        return RelationshipRouter(
            answer_store=self._questionnaire_store.answer_store,
            relationship_store=self.relationship_store,
            section_id=self._current_location.section_id,
            list_name=list_name,
            list_item_ids=list_items,
            relationships_block_id=self.relationships_block["id"],
            unrelated_block_id=self.unrelated_block_id,
            unrelated_answer_id=self.unrelated_answer_id,
            unrelated_no_answer_values=self.unrelated_no_answer_values,
        )

    def _get_routing_path(self):
        return self.router.routing_path(section_id=self.parent_location.section_id)

    def is_location_valid(self):
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
        return self.relationship_router.get_first_location().url()

    def get_last_location_url(self):
        return self.relationship_router.get_last_location().url()

    def get_previous_location_url(self):
        previous_location = self.relationship_router.get_previous_location(
            self._current_location
        )
        if previous_location:
            return previous_location.url()

        return self.router.get_previous_location_url(
            self.parent_location, self._routing_path
        )

    def get_next_location_url(self):
        next_location = self.relationship_router.get_next_location(
            self._current_location
        )
        if next_location:
            return next_location.url()

        return self.router.get_next_location_url(
            self.parent_location, self._routing_path, self._return_to
        )
