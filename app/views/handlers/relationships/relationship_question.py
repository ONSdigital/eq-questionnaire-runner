from functools import cached_property

from werkzeug.datastructures import ImmutableDict

from app.data_models.relationship_store import RelationshipDict, RelationshipStore
from app.questionnaire.location import Location, SectionKey
from app.questionnaire.relationship_router import RelationshipRouter
from app.questionnaire.router import RoutingPath
from app.views.handlers.question import Question


class RelationshipQuestion(Question):
    @cached_property
    def relationships_block(self) -> ImmutableDict | None:
        return self._schema.get_block(self.block["id"])

    @cached_property
    def relationships_answer_id(self) -> str:
        return self._schema.get_first_answer_id_for_block(
            # Type ignore: block must exist when this is called
            self.relationships_block["id"]  # type: ignore
        )

    @property
    def parent_location(self) -> Location:
        return Location(
            section_id=self._current_location.section_id,
            # Type ignore: block must exist when this is called
            block_id=self.relationships_block["id"],  # type: ignore
        )

    @cached_property
    def unrelated_block_id(self) -> str | None:
        # Type ignore: called when relationships_block already exists
        value: str = self.relationships_block.get("unrelated_block", {}).get("id")  # type: ignore
        return value

    @cached_property
    def unrelated_answer_id(self) -> str | None:
        if self.unrelated_block_id:
            return self._schema.get_first_answer_id_for_block(self.unrelated_block_id)
        return None

    @cached_property
    def unrelated_no_answer_values(self) -> list[str] | None:
        if self.unrelated_answer_id:
            return self._schema.get_unrelated_block_no_answer_values(
                self.unrelated_answer_id
            )

    @cached_property
    def relationship_store(self) -> RelationshipStore:
        answer = self._questionnaire_store.answer_store.get_answer(
            self.relationships_answer_id
        )
        if answer:
            # Type ignore: for a relationship question the answer will always be a list of RelationshipDict
            answer_value: list[RelationshipDict] = answer.value  # type: ignore
            return RelationshipStore(answer_value)
        return RelationshipStore()

    @property
    def relationship_router(self) -> RelationshipRouter:
        # Type ignore: list will be populated at this point as it is required to build relationship
        list_name = self.relationships_block["for_list"]  # type: ignore
        list_items = self._questionnaire_store.list_store[list_name].items

        return RelationshipRouter(
            answer_store=self._questionnaire_store.answer_store,
            relationship_store=self.relationship_store,
            section_id=self._current_location.section_id,
            list_name=list_name,
            list_item_ids=list_items,
            # Type ignore: block must exist before getting to this point
            relationships_block_id=self.relationships_block["id"],  # type: ignore
            unrelated_block_id=self.unrelated_block_id,
            unrelated_answer_id=self.unrelated_answer_id,
            unrelated_no_answer_values=self.unrelated_no_answer_values,
        )

    def _get_routing_path(self) -> RoutingPath:
        return self.router.routing_path(
            SectionKey(section_id=self.parent_location.section_id, list_item_id=None)
        )

    def is_location_valid(self) -> bool:
        can_access_parent_location = self.router.can_access_location(
            self.parent_location, self._routing_path
        )
        can_access_relationship_location = self.relationship_router.can_access_location(
            self._current_location  # type: ignore
        )
        if not can_access_parent_location or not can_access_relationship_location:
            return False
        return True

    def get_first_location_url(self) -> str:
        return self.relationship_router.get_first_location().url()

    def get_last_location_url(self) -> str:
        return self.relationship_router.get_last_location().url()

    def get_previous_location_url(self) -> str:
        previous_location = self.relationship_router.get_previous_location(
            # Type ignore: block will determine type of location to be relationship location
            self._current_location  # type: ignore
        )
        if previous_location:
            return previous_location.url()

        return self.router.get_previous_location_url(  # type: ignore
            self.parent_location, self._routing_path
        )

    def get_next_location_url(self) -> str:
        next_location = self.relationship_router.get_next_location(
            # Type ignore: block will determine type of location to be relationship location
            self._current_location  # type: ignore
        )
        if next_location:
            return next_location.url()

        return self.router.get_next_location_url(
            self.parent_location, self._routing_path, self._return_to
        )
