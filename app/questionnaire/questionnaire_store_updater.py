from collections import defaultdict
from itertools import combinations
from typing import Any, Dict, List, Mapping, Optional, Tuple, Union

from app.data_models import AnswerValueTypes, QuestionnaireStore
from app.data_models.answer_store import Answer
from app.data_models.progress_store import CompletionStatus, SectionKeyType
from app.questionnaire import QuestionnaireSchema
from app.questionnaire.location import Location
from app.questionnaire.questionnaire_schema import AnswerDependent


class QuestionnaireStoreUpdater:
    """Component responsible for any actions that need to happen as a result of updating the questionnaire_store"""

    EMPTY_ANSWER_VALUES: Tuple = (None, [], "", {})

    def __init__(
        self,
        current_location: Location,
        schema: QuestionnaireSchema,
        questionnaire_store: QuestionnaireStore,
        current_question: Mapping[str, Any],
    ):
        self._current_location = current_location
        self._current_question = current_question or {}
        self._schema = schema
        self._questionnaire_store = questionnaire_store
        self._answer_store = self._questionnaire_store.answer_store
        self._list_store = self._questionnaire_store.list_store
        self._progress_store = self._questionnaire_store.progress_store

        self.dependent_block_id_by_section_key: Mapping[
            SectionKeyType, set[str]
        ] = defaultdict(set)

    def save(self):
        if self.is_dirty():
            self._questionnaire_store.save()

    def is_dirty(self):
        if (
            self._answer_store.is_dirty
            or self._list_store.is_dirty
            or self._progress_store.is_dirty
        ):
            return True
        return False

    def update_relationships_answer(
        self,
        relationship_store,
        relationships_answer_id,
    ):
        self._answer_store.add_or_update(
            Answer(relationships_answer_id, relationship_store.serialize())
        )

    def remove_completed_relationship_locations_for_list_name(
        self, list_name: str
    ) -> None:
        target_relationship_collectors = self._get_relationship_collectors_by_list_name(
            list_name
        )
        if target_relationship_collectors:
            for target in target_relationship_collectors:
                block_id = target["id"]
                section_id = self._schema.get_section_for_block_id(block_id)["id"]  # type: ignore
                self.remove_completed_location(Location(section_id, block_id))

    def update_relationship_question_completeness(self, list_name: str) -> None:
        relationship_collectors = self._get_relationship_collectors_by_list_name(
            list_name
        )

        if not relationship_collectors:
            return None

        list_items = self._list_store[list_name]

        for collector in relationship_collectors:

            relationship_answer_id = self._schema.get_first_answer_id_for_block(
                collector["id"]
            )
            relationship_answers = self._get_relationships_in_answer_store(
                relationship_answer_id
            )

            if relationship_answers:
                pairs = {
                    (answer["list_item_id"], answer["to_list_item_id"])
                    for answer in relationship_answers
                }

                expected_pairs = set(combinations(list_items, 2))
                if expected_pairs == pairs:
                    section_id = self._schema.get_section_for_block_id(collector["id"])[
                        "id"
                    ]  # type: ignore
                    location = Location(section_id, collector["id"])
                    self.add_completed_location(location)

    def _get_relationship_collectors_by_list_name(self, list_name: str):
        return self._schema.get_relationship_collectors_by_list_name(list_name)

    def _get_relationships_in_answer_store(self, relationship_answer_id: str):
        return self._answer_store.get_answer(relationship_answer_id).value  # type: ignore

    def remove_answers(self, answer_ids: List, list_item_id: str = None):
        for answer_id in answer_ids:
            self._answer_store.remove_answer(answer_id, list_item_id=list_item_id)

    def add_primary_person(self, list_name):
        self.remove_completed_relationship_locations_for_list_name(list_name)

        if self._list_store[list_name].primary_person:
            return self._list_store[list_name].primary_person

        # If a primary person was initially answered negatively, then changed to positive,
        # the location must be removed from the progress store.
        self.remove_completed_location(self._current_location)

        return self._list_store.add_list_item(list_name, primary_person=True)

    def add_list_item(self, list_name):
        new_list_item_id = self._list_store.add_list_item(list_name)
        self.remove_completed_relationship_locations_for_list_name(list_name)
        return new_list_item_id

    def remove_primary_person(self, list_name: str):
        """Remove the primary person and all of their answers.
        Any context for the primary person will be removed
        """
        list_item_id = self._list_store[list_name].primary_person
        if list_item_id:
            self.remove_list_item_and_answers(list_name, list_item_id)

    def remove_list_item_and_answers(self, list_name: str, list_item_id: str):
        """Remove answers from the answer store and update the list store to remove it.
        Any related relationship answers are re-evaluated for completeness.
        """
        self._list_store.delete_list_item(list_name, list_item_id)

        self._answer_store.remove_all_answers_for_list_item_id(
            list_item_id=list_item_id
        )

        answers = self.get_relationship_answers_for_list_name(list_name)
        if answers:
            self.remove_relationship_answers_for_list_item_id(list_item_id, answers)
            self.update_relationship_question_completeness(list_name)

        self._progress_store.remove_progress_for_list_item_id(list_item_id=list_item_id)

    def get_relationship_answers_for_list_name(
        self, list_name: str
    ) -> Union[List[Answer], None]:
        associated_relationship_collectors = (
            self._get_relationship_collectors_by_list_name(list_name)
        )
        if not associated_relationship_collectors:
            return None

        relationship_answer_ids = [
            self._schema.get_first_answer_id_for_block(block["id"])
            for block in associated_relationship_collectors
        ]

        return self._answer_store.get_answers_by_answer_id(relationship_answer_ids)

    def update_same_name_items(
        self, list_name: str, same_name_answer_ids: Optional[List[str]]
    ):
        if not same_name_answer_ids:
            return

        same_name_items = set()
        people_names: Dict[str, list] = {}

        list_model = self._questionnaire_store.list_store[list_name]

        for current_list_item_id in list_model:
            answers = self._questionnaire_store.answer_store.get_answers_by_answer_id(
                answer_ids=same_name_answer_ids, list_item_id=current_list_item_id
            )
            current_names = [answer.value.casefold() for answer in answers if answer]  # type: ignore
            current_list_item_name = " ".join(current_names)

            if matching_list_item_id := people_names.get(current_list_item_name):
                same_name_items |= {current_list_item_id, matching_list_item_id}
            else:
                people_names[current_list_item_name] = current_list_item_id  # type: ignore

        list_model.same_name_items = list(same_name_items)  # type: ignore

    def remove_relationship_answers_for_list_item_id(
        self, list_item_id: str, answers: List
    ) -> None:
        for answer in answers:
            answers_to_keep = [
                value
                for value in answer.value
                if list_item_id not in {value["to_list_item_id"], value["list_item_id"]}
            ]
            answer.value = answers_to_keep
            self._answer_store.add_or_update(answer)

    def add_completed_location(self, location: Optional[Location] = None):
        if not self._progress_store.is_routing_backwards:
            location = location or self._current_location
            self._progress_store.add_completed_location(location)

    def remove_completed_location(self, location: Optional[Location] = None) -> bool:
        location = location or self._current_location
        return self._progress_store.remove_completed_location(location)

    def update_section_status(
        self, is_complete: bool, section_id: str, list_item_id: Optional[str] = None
    ):
        status = (
            CompletionStatus.COMPLETED if is_complete else CompletionStatus.IN_PROGRESS
        )
        self._progress_store.update_section_status(status, section_id, list_item_id)

    def _update_answer(
        self,
        answer_id: str,
        list_item_id: Optional[str],
        answer_value: AnswerValueTypes,
    ) -> bool:
        answer_value_to_store = (
            {
                key: value
                for key, value in answer_value.items()
                if value not in self.EMPTY_ANSWER_VALUES
            }
            if isinstance(answer_value, dict)
            else answer_value
        )

        if answer_value_to_store in self.EMPTY_ANSWER_VALUES:
            return self._answer_store.remove_answer(
                answer_id, list_item_id=list_item_id
            )

        return self._answer_store.add_or_update(
            Answer(
                answer_id=answer_id,
                list_item_id=list_item_id,
                value=answer_value_to_store,
            )
        )

    def _capture_dependencies_for_answer(self, answer_id: str) -> None:
        """Captures a unique list of block ids that are dependents of the provided answer id.

        The block_ids are mapped to the section key. Dependencies in a repeating section use the list items
        for the repeating list when creating the section key.

        Blocks are captured regardless of whether they are complete. This avoids fetching the completed blocks
        multiples times, as you may have multiple dependencies for one block which may also apply to each item in the list.
        However, when updating the progress store, the block ids are checked to ensure they exist in the progress store.
        """
        dependencies: set[AnswerDependent] = self._schema.answer_dependencies.get(
            answer_id, set()
        )

        for dependency in dependencies:
            if dependency.for_list:
                list_item_ids: Union[list[str], list[None]] = self._list_store[
                    dependency.for_list
                ].items
            else:
                list_item_ids = [None]

            for list_item_id in list_item_ids:
                if dependency.answer_id:  # pragma: no cover
                    # :TODO: Remove answer. Required for dynamic options
                    raise NotImplementedError

                self.dependent_block_id_by_section_key[
                    (dependency.section_id, list_item_id)
                ].add(dependency.block_id)

    def update_answers(
        self, form_data: Mapping[str, Any], list_item_id: Optional[str] = None
    ) -> None:
        list_item_id = list_item_id or self._current_location.list_item_id
        answer_ids_for_question = self._schema.get_answer_ids_for_question(
            self._current_question
        )

        for answer_id, answer_value in form_data.items():
            if answer_id not in answer_ids_for_question:
                continue

            answer_updated = self._update_answer(answer_id, list_item_id, answer_value)
            if answer_updated:
                self._capture_dependencies_for_answer(answer_id)

    def update_progress_for_dependant_sections(self) -> None:
        """Removes dependent blocks from the progress store and updates the progress to IN_PROGRESS.

        Section progress is not updated for the current location as it is handled by `handle_post` on block handlers.

        When updating the progress store, the routing path is not re-evaluated because
        removing previously completed blocks means the section can't be complete.
        """
        for (
            section_key,
            blocks_to_remove,
        ) in self.dependent_block_id_by_section_key.items():
            if section_key not in self._progress_store.started_section_keys():
                continue

            section_id, list_item_id = section_key

            blocks_removed = False
            for block_id in blocks_to_remove:
                location = Location(
                    section_id=section_id,
                    list_item_id=list_item_id,
                    block_id=block_id,
                )
                blocks_removed |= self.remove_completed_location(location)

            if blocks_removed and (
                section_id != self._current_location.section_id
                or list_item_id != self._current_location.list_item_id
            ):
                self.update_section_status(
                    is_complete=False,
                    section_id=section_id,
                    list_item_id=list_item_id,
                )
