from typing import Iterable, Mapping

from app.data_models import QuestionnaireStore
from app.questionnaire import QuestionnaireSchema
from app.questionnaire.base_questionnaire_store_updater import (
    BaseQuestionnaireStoreUpdater,
)
from app.questionnaire.questionnaire_schema import AnswerDependent
from app.questionnaire.router import Router
from app.utilities.types import DependentSection, LocationType


class QuestionnaireStoreUpdater(BaseQuestionnaireStoreUpdater):
    """
    Component responsible for any actions that need to happen as a result of updating the questionnaire_store
    """

    EMPTY_ANSWER_VALUES: tuple[None, list, str, dict] = (None, [], "", {})

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

    def _get_list_item_ids_for_dependency(
        self, dependency: AnswerDependent, is_repeating_answer: bool | None = False
    ) -> list[str] | list[None]:
        if dependency.for_list:
            list_item_ids: list[str] | list[None]

            if is_repeating_answer:
                # If the source answer is repeating, then we must be in the current repeating section.
                # A repeating answer should only ever be depended on by itself.
                list_item_ids = [self._current_location.list_item_id]  # type: ignore
            else:
                list_item_ids = self._list_store[dependency.for_list].items
        else:
            list_item_ids = [None]

        return list_item_ids

    def _capture_section_dependencies_progress_value_source_for_current_section(
        self,
    ) -> None:
        """
        Captures a unique list of section ids that are dependents of the current section, for progress value sources.
        """
        dependent_sections: Iterable = self._schema.when_rules_section_dependencies_by_section_for_progress_value_source.get(
            self._current_location.section_id, set()
        )
        self._update_section_dependencies(dependent_sections)

    def _capture_section_dependencies_progress_value_source_for_current_block(
        self,
    ) -> None:
        """
        Captures a unique list of section ids that are dependents of the current block, for progress value sources.
        """
        # Type ignore: Added as block_id will exist at this point
        dependent_sections: Iterable = self._schema.when_rules_block_dependencies_by_section_for_progress_value_source.get(
            self._current_location.section_id, {}
        ).get(
            self._current_location.block_id, set()  # type: ignore
        )

        self._update_section_dependencies(dependent_sections)

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
                self.capture_progress_section_dependencies()

    def capture_progress_section_dependencies(self) -> None:
        self._capture_section_dependencies_progress_value_source_for_current_block()
        self._capture_section_dependencies_progress_value_source_for_current_section()

    def _is_current_location(self, section_id: str, list_item_id: str | None) -> bool:
        """Used by remove_dependent_blocks_and_capture_dependent_sections to determine if section_id and list_item_id
        don't match the current location, and therefore need to be added as a dependent section
        """
        return (
            section_id == self._current_location.section_id
            and list_item_id == self._current_location.list_item_id
        )

    def _get_section_ids_dependent_on_list(self, list_name: str) -> list[str]:
        return [
            *super()._get_section_ids_dependent_on_list(list_name),
            self._current_location.section_id,
        ]
