from typing import List, Optional

from app.data_models.answer_store import AnswerStore
from app.data_models.relationship_store import RelationshipStore
from app.questionnaire.relationship_location import RelationshipLocation


class RelationshipRouter:
    UNRELATED_RELATIONSHIP_VALUE = "Unrelated"

    def __init__(
        self,
        answer_store: AnswerStore,
        relationship_store: RelationshipStore,
        section_id: str,
        list_name: str,
        list_item_ids: List[str],
        relationships_block_id: str,
        unrelated_block_id: Optional[str] = None,
        unrelated_answer_id: Optional[str] = None,
        unrelated_no_answer_values: Optional[List[str]] = None,
    ):
        self.answer_store = answer_store
        self.relationship_store = relationship_store
        self.section_id = section_id
        self.list_name = list_name
        self.list_item_ids = list_item_ids
        self.relationships_block_id = relationships_block_id
        self.unrelated_block_id = unrelated_block_id
        self.unrelated_answer_id = unrelated_answer_id
        self.unrelated_no_answer_values = unrelated_no_answer_values
        self.path = self._relationships_routing_path()

    def can_access_location(self, location):
        return location in self.path

    def get_first_location(self):
        return self.path[0]

    def get_last_location(self):
        return self.path[-1]

    def get_next_location(self, location):
        try:
            location_index = self.path.index(location)
            return self.path[location_index + 1]
        except IndexError:
            return None

    def get_previous_location(self, location):
        location_index = self.path.index(location)
        if not location_index:
            return None
        return self.path[location_index - 1]

    def _relationships_routing_path(self):
        path = []
        for from_index, from_list_item_id in enumerate(self.list_item_ids):
            path += self._individual_relationships_routing_path(
                from_list_item_id=from_list_item_id,
                to_list_item_ids=self.list_item_ids[from_index + 1 :],
            )

        return path

    def _individual_relationships_routing_path(
        self, from_list_item_id, to_list_item_ids
    ):
        path = []
        number_of_unrelated_relationships = 0
        number_of_relationships_left = len(to_list_item_ids)
        unrelated_block_in_path = False
        for to_item_id in to_list_item_ids:
            if (
                self.unrelated_block_id
                and number_of_relationships_left >= 2
                and number_of_unrelated_relationships == 2
                and not unrelated_block_in_path
            ):
                path.append(
                    RelationshipLocation(
                        section_id=self.section_id,
                        block_id=self.unrelated_block_id,
                        list_item_id=from_list_item_id,
                        list_name=self.list_name,
                    )
                )
                unrelated_block_in_path = True
                unrelated_answer = self.answer_store.get_answer(
                    self.unrelated_answer_id, from_list_item_id
                )
                if (
                    unrelated_answer
                    and unrelated_answer.value in self.unrelated_no_answer_values
                ):
                    return path

            path.append(
                RelationshipLocation(
                    section_id=self.section_id,
                    block_id=self.relationships_block_id,
                    list_item_id=from_list_item_id,
                    to_list_item_id=to_item_id,
                    list_name=self.list_name,
                )
            )
            relationship_answer = self.relationship_store.get_relationship(
                from_list_item_id, to_item_id
            )
            if (
                relationship_answer
                and relationship_answer.relationship
                == self.UNRELATED_RELATIONSHIP_VALUE
            ):
                number_of_unrelated_relationships += 1

            number_of_relationships_left -= 1

        return path
