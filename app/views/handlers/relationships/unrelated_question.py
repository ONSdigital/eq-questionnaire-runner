from functools import cached_property

from app.views.handlers.relationships.relationship_question import RelationshipQuestion


class UnrelatedQuestion(RelationshipQuestion):
    @cached_property
    def list_name(self):
        return self.block["list_summary"]["for_list"]

    @cached_property
    def relationships_block(self):
        parent_block_id = self._schema.parent_id_map[self.block["id"]]
        return self._schema.get_block(parent_block_id)

    @cached_property
    def unrelated_block_id(self):
        return self.block["id"]

    def get_list_summary_context(self):
        return self.list_context(
            self.rendered_block["list_summary"]["summary"],
            self.list_name,
            for_list_item_ids=self.get_remaining_relationships_for_individual(),
        )

    def get_remaining_relationships_for_individual(self):
        list_model = self._questionnaire_store.list_store[self.list_name]
        previous_location = self.relationship_router.get_previous_location(
            self.current_location
        )
        previous_item_index = list_model.index(previous_location.to_list_item_id)
        return list_model[previous_item_index + 1 :]

    def handle_post(self):
        self.questionnaire_store_updater.update_answers(
            self.form.data, list_item_id=self.current_location.list_item_id
        )
        self.questionnaire_store_updater.save()
