from typing import Mapping, MutableMapping

from app.data_models.relationship_store import Relationship
from app.questionnaire.location import Location
from app.views.handlers.relationships.relationship_question import RelationshipQuestion


class RelationshipCollector(RelationshipQuestion):
    def is_location_valid(self) -> bool:
        if isinstance(self._current_location, Location):
            return self.router.can_access_location(
                self._current_location, self._routing_path
            )

        return super().is_location_valid()

    def handle_post(self) -> None:
        relationship_answer = self.form.data.get(self.relationships_answer_id)
        relationship = Relationship(
            # Type ignore: handle_post is only called from relationships endpoint and location class is assigned to RelationshipLocation
            self._current_location.list_item_id,  # type: ignore
            self._current_location.to_list_item_id,  # type: ignore
            relationship_answer,
        )
        self.relationship_store.add_or_update(relationship)

        if self.relationship_store.is_dirty:
            self.questionnaire_store_updater.update_relationships_answer(
                relationship_store=self.relationship_store,
                relationships_answer_id=self.relationships_answer_id,
            )

        if self._is_last_relationship():
            self.questionnaire_store_updater.add_completed_location(
                location=self.parent_location
            )
            self._update_section_completeness(location=self.parent_location)

        self.questionnaire_store_updater.save()

    def _get_answers_for_question(self, question_json: Mapping) -> dict:
        relationship = self.relationship_store.get_relationship(
            # relationship only used if these exist. RelationshipLocation wil already be determined.
            self._current_location.list_item_id,  # type: ignore
            self._current_location.to_list_item_id,  # type: ignore
        )
        if relationship:
            return {self.relationships_answer_id: relationship.relationship}
        return {}

    def _is_last_relationship(self) -> bool:
        if self.relationship_router.get_next_location(self._current_location):  # type: ignore
            return False
        return True

    def _resolve_custom_page_title_vars(self) -> MutableMapping:
        page_title_vars = super()._resolve_custom_page_title_vars()

        if to_list_item_position := self.current_location.to_list_item_id:  # type: ignore
            page_title_vars["to_list_item_position"] = (
                self._questionnaire_store.data_stores.list_store.list_item_position(
                    # Type ignore: list_name populated at this stage
                    self.current_location.list_name,  # type: ignore
                    to_list_item_position,
                )
            )

        return page_title_vars
