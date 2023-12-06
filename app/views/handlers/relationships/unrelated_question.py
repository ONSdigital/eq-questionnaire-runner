from functools import cached_property

from werkzeug.datastructures import ImmutableDict

from app.data_models.relationship_store import Relationship
from app.views.handlers.relationships.relationship_question import RelationshipQuestion


class UnrelatedQuestion(RelationshipQuestion):
    @cached_property
    def list_name(self) -> str:
        value: str = self.block["list_summary"]["for_list"]
        return value

    @cached_property
    def relationships_block(self) -> ImmutableDict | None:
        parent_block_id = self._schema.parent_id_map[self.block["id"]]
        return self._schema.get_block(parent_block_id)

    @cached_property
    def unrelated_block_id(self) -> str | None:
        value: str | None = self.block["id"]
        return value

    def get_list_summary_context(self) -> dict[str, dict]:
        return self.list_context(
            summary_definition=self.rendered_block["list_summary"]["summary"],
            for_list=self.list_name,
            section_id=self.current_location.section_id,
            has_repeating_blocks=bool(self.rendered_block.get("repeating_blocks")),
            for_list_item_ids=self.get_remaining_relationships_for_individual(),
        )

    def get_remaining_relationships_for_individual(self) -> list[str]:
        """
        Returns a list of 'to' item ids for the remaining relationships.
        These relationships won't be on the path if the user has selected
        "No" to the unrelated question, so we get them from the list store.
        """
        list_model = self._questionnaire_store.data_stores.list_store[self.list_name]
        previous_location = self.relationship_router.get_previous_location(
            # Type ignore: block will determine type of location to be relationship location
            self.current_location  # type: ignore
        )
        previous_item_index = list_model.index(previous_location.to_list_item_id)  # type: ignore
        return list_model[previous_item_index + 1 :]

    def handle_post(self) -> None:
        if answer_action := self._get_answer_action():
            self.handle_answer_action(answer_action["type"])

        self.questionnaire_store_updater.update_answers(
            self.form.data, list_item_id=self.current_location.list_item_id
        )
        self.questionnaire_store_updater.save()

    def handle_answer_action(self, answer_action_type: str) -> None:
        from_list_item_id = self.current_location.list_item_id

        if answer_action_type == "RemoveUnrelatedRelationships":
            for to_list_item_id in self.get_remaining_relationships_for_individual():
                relationship = self.relationship_store.get_relationship(
                    # Type ignore: from_list_item_id populated at this stage
                    from_list_item_id,  # type: ignore
                    to_list_item_id,
                )
                if relationship and (
                    relationship.relationship
                    == self.relationship_router.UNRELATED_RELATIONSHIP_VALUE
                ):
                    self.relationship_store.remove_relationship(
                        from_list_item_id, to_list_item_id  # type: ignore
                    )

        elif answer_action_type == "AddUnrelatedRelationships":
            for to_list_item_id in self.get_remaining_relationships_for_individual():
                relationship = Relationship(
                    # Type ignore: from_list_item_id populated at this stage
                    list_item_id=from_list_item_id,  # type: ignore
                    to_list_item_id=to_list_item_id,
                    relationship=self.relationship_router.UNRELATED_RELATIONSHIP_VALUE,
                )
                self.relationship_store.add_or_update(relationship)

        if self.relationship_store.is_dirty:
            self.questionnaire_store_updater.update_relationships_answer(
                relationship_store=self.relationship_store,
                relationships_answer_id=self.relationships_answer_id,
            )
