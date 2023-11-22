from typing import Mapping

from app.data_models import QuestionnaireStore
from app.questionnaire import QuestionnaireSchema
from app.questionnaire.base_questionnaire_store_updater import (
    BaseQuestionnaireStoreUpdater,
)
from app.questionnaire.questionnaire_schema import Dependent
from app.questionnaire.router import Router
from app.utilities.types import LocationType


class QuestionnaireStoreUpdater(BaseQuestionnaireStoreUpdater):
    """Component responsible for any actions that need to happen as a result of updating the questionnaire_store"""

    def __init__(
        self,
        current_location: LocationType,
        schema: QuestionnaireSchema,
        questionnaire_store: QuestionnaireStore,
        router: Router,
        current_question: Mapping | None,
    ):
        self._current_location = current_location
        self._current_question = current_question or {}
        super().__init__(
            schema=schema, questionnaire_store=questionnaire_store, router=router
        )

    def add_primary_person(self, list_name: str) -> str:
        self.remove_completed_relationship_locations_for_list_name(list_name)

        if primary_person := self._list_store[list_name].primary_person:
            return primary_person

        # If a primary person was initially answered negatively, then changed to positive,
        # the location must be removed from the progress store.
        self.remove_completed_location(self._current_location)

        return self._list_store.add_list_item(list_name, primary_person=True)

    def remove_primary_person(self, list_name: str) -> None:
        """Remove the primary person and all of their answers.
        Any context for the primary person will be removed
        """
        if list_item_id := self._list_store[list_name].primary_person:
            self.remove_list_item_data(list_name, list_item_id)

    def add_completed_location(self, location: LocationType | None = None) -> None:
        if not self._progress_store.is_routing_backwards:
            location = location or self._current_location
            self._progress_store.add_completed_location(location)

    def remove_completed_location(self, location: LocationType | None = None) -> bool:
        location = location or self._current_location
        return self._progress_store.remove_completed_location(location)

    def _capture_block_dependencies_for_answer(self, answer_id: str) -> None:
        """Captures a unique list of block ids that are dependents of the provided answer id."""
        dependencies: set[Dependent] = self._schema.answer_dependencies.get(
            answer_id, set()
        )
        is_repeating_answer = self._schema.is_answer_in_repeating_section(answer_id)

        for dependent in dependencies:
            list_item_ids = self._get_list_item_ids_for_answer_dependency(
                dependent, is_repeating_answer
            )
            self._capture_block_dependent(dependent, list_item_ids)

    def _get_list_item_ids_for_answer_dependency(
        self, dependency: Dependent, is_repeating_answer: bool | None = False
    ) -> list[str] | list[None]:
        """
        Gets the list item ids that relate to the dependency of the answer.
        If the dependency is repeating, and so is the answer, then we must be in that repeating section,
        so the only relevant list item id is the current one.
        If the answer is not repeating, but the dependency is, then all list item ids need including.
        """
        if dependency.for_list:
            if is_repeating_answer:
                # Type ignore: in this scenario the list item id must exist
                return [self._current_location.list_item_id]  # type: ignore
            return self._list_store[dependency.for_list].items
        return [None]

    def update_answers(
        self, form_data: Mapping, list_item_id: str | None = None
    ) -> None:
        list_item_id = list_item_id or self._current_location.list_item_id
        answers_by_answer_id = self._schema.get_answers_for_question_by_id(
            self._current_question
        )

        for answer_id, answer_value in form_data.items():
            if answer_id not in answers_by_answer_id:
                continue

            resolved_answer = answers_by_answer_id[answer_id]
            answer_id_to_use = resolved_answer.get("original_answer_id") or answer_id
            list_item_id_to_use = resolved_answer.get("list_item_id") or list_item_id

            if self._update_answer(answer_id_to_use, list_item_id_to_use, answer_value):
                self._capture_section_dependencies_for_answer(answer_id_to_use)
                self._capture_block_dependencies_for_answer(answer_id_to_use)

        if self._answer_store.is_dirty:
            self.capture_progress_section_dependencies()

    def capture_progress_section_dependencies(self) -> None:
        """
        Captures a unique list of section ids that are dependents of the current section or block, for progress value sources.
        """
        self._capture_section_dependencies_progress_value_source_for_section(
            self._current_location.section_id
        )
        # Type ignore: block id will exist when at any time this is called
        self._capture_section_dependencies_progress_value_source_for_block(
            section_id=self._current_location.section_id,
            block_id=self._current_location.block_id,  # type: ignore
        )

    def is_current_section(self, section_id: str, list_item_id: str | None) -> bool:
        """Overwritten by QuestionnaireStoreUpdater to return True if the location is the current section"""
        return (
            section_id == self._current_location.section_id
            and list_item_id == self._current_location.list_item_id
        )
