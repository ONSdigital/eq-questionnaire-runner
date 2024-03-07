from collections import defaultdict
from itertools import combinations
from typing import Iterable, Mapping, MutableMapping, Sequence

from ordered_set import OrderedSet
from werkzeug.datastructures import ImmutableDict

from app.data_models import (
    AnswerValueTypes,
    CompletionStatus,
    QuestionnaireStore,
    SupplementaryDataStore,
)
from app.data_models.answer_store import Answer
from app.data_models.relationship_store import RelationshipDict, RelationshipStore
from app.questionnaire import QuestionnaireSchema
from app.questionnaire.location import Location, SectionKey
from app.questionnaire.questionnaire_schema import Dependent
from app.questionnaire.router import Router
from app.utilities.types import (
    DependentSection,
    LocationType,
    SupplementaryDataListMapping,
)


class QuestionnaireStoreUpdaterBase:
    """Component responsible for any actions that need to happen as a result of updating the questionnaire_store
    his should only be used over the QuestionnaireStoreUpdater if location is unknown"""

    EMPTY_ANSWER_VALUES: tuple[None, list, str, dict] = (None, [], "", {})

    def __init__(
        self,
        schema: QuestionnaireSchema,
        questionnaire_store: QuestionnaireStore,
        router: Router,
    ):
        self._schema = schema
        self._questionnaire_store = questionnaire_store
        self._answer_store = self._questionnaire_store.data_stores.answer_store
        self._list_store = self._questionnaire_store.data_stores.list_store
        self._progress_store = self._questionnaire_store.data_stores.progress_store
        self._router = router

        self.dependent_block_id_by_section_key: Mapping[SectionKey, set[str]] = (
            defaultdict(set)
        )
        self.dependent_sections: set[DependentSection] = set()

    @property
    def _supplementary_data_store(self) -> SupplementaryDataStore:
        return self._questionnaire_store.data_stores.supplementary_data_store

    @_supplementary_data_store.setter
    def _supplementary_data_store(self, store: SupplementaryDataStore) -> None:
        self._questionnaire_store.data_stores.supplementary_data_store = store

    def save(self) -> None:
        if self.is_dirty():
            self._questionnaire_store.save()

    def is_dirty(self) -> bool:
        return bool(
            (
                self._answer_store.is_dirty
                or self._list_store.is_dirty
                or self._progress_store.is_dirty
            )
        )

    def update_relationships_answer(
        self,
        relationship_store: RelationshipStore,
        relationships_answer_id: str,
    ) -> None:
        self._answer_store.add_or_update(
            # Type ignore: serialize returns a list of typed dicts, so it is a valid answer type
            Answer(relationships_answer_id, relationship_store.serialize())  # type: ignore
        )

    def remove_completed_relationship_locations_for_list_name(
        self, list_name: str
    ) -> None:
        if target_relationship_collectors := self._get_relationship_collectors_by_list_name(
            list_name
        ):
            for target in target_relationship_collectors:
                block_id = target["id"]
                section_id = self._schema.get_section_for_block_id(block_id)["id"]  # type: ignore
                self.remove_completed_location(Location(section_id, block_id))

    def _update_relationship_question_completeness(self, list_name: str) -> None:
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
            if relationship_answers := self._get_relationships_in_answer_store(
                relationship_answer_id
            ):
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

    def _get_relationship_collectors_by_list_name(
        self, list_name: str
    ) -> list[ImmutableDict] | None:
        return self._schema.get_relationship_collectors_by_list_name(list_name)

    def _get_relationships_in_answer_store(
        self, relationship_answer_id: str
    ) -> list[RelationshipDict]:
        return self._answer_store.get_answer(relationship_answer_id).value  # type: ignore

    def remove_answers(
        self, answer_ids: list[str], list_item_id: str | None = None
    ) -> None:
        for answer_id in answer_ids:
            self._answer_store.remove_answer(answer_id, list_item_id=list_item_id)

    def add_list_item(self, list_name: str) -> str:
        new_list_item_id = self._list_store.add_list_item(list_name)
        self.remove_completed_relationship_locations_for_list_name(list_name)
        return new_list_item_id

    def remove_list_item_data(self, list_name: str, list_item_id: str) -> None:
        """Remove answers from the answer store, remove list item progress from the progress store and update the list store to remove it.
        Any related relationship answers are re-evaluated for completeness.
        """
        self._list_store.delete_list_item(list_name, list_item_id)

        self._answer_store.remove_all_answers_for_list_item_ids(list_item_id)

        if answers := self._get_relationship_answers_for_list_name(list_name):
            self._remove_relationship_answers_for_list_item_id(list_item_id, answers)
            self._update_relationship_question_completeness(list_name)

        self._progress_store.remove_progress_for_list_item_id(list_item_id=list_item_id)

    def remove_list_data(self, list_name: str) -> None:
        """Delete entire list and remove any associated answers"""
        self._answer_store.remove_all_answers_for_list_item_ids(
            *self._list_store[list_name].items
        )
        self._list_store.delete_list(list_name)

    def capture_dependencies_for_list_change(self, list_name: str) -> None:
        """
        Captures the dependencies when an item is added to or removed from the given list.
        Any list collector sections will be affected by the change as well as other sections using when rules
        """
        self._capture_block_dependencies_for_list(list_name)
        section_ids = self._schema.get_when_rule_section_dependencies_for_list(
            list_name
        )
        section_ids.update(
            self._schema.list_collector_section_ids_by_list_name.get(list_name, set())
        )

        for section_key in self.started_section_keys(section_ids=section_ids):
            # Only add sections which are repeated sections for this list, or the section in which this list is collected
            # Prevents list item progresses being added as dependants as these are captured by started_section_keys(section_ids=section_ids)
            if section_key.list_item_id and not self._schema.get_repeat_for_section(
                section_key.section_id
            ):
                continue
            self.dependent_sections.add(DependentSection(**section_key.to_dict()))

    def _get_relationship_answers_for_list_name(
        self, list_name: str
    ) -> list[Answer] | None:
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
        self, list_name: str, same_name_answer_ids: list[str] | None
    ) -> None:
        if not same_name_answer_ids:
            return

        same_name_items = set()
        people_names: dict[str, str] = {}

        list_model = self._list_store[list_name]

        for current_list_item_id in list_model:
            answers = self._answer_store.get_answers_by_answer_id(
                answer_ids=same_name_answer_ids, list_item_id=current_list_item_id
            )
            current_names = [answer.value.casefold() for answer in answers if answer]  # type: ignore
            current_list_item_name = " ".join(current_names)

            if matching_list_item_id := people_names.get(current_list_item_name):
                same_name_items |= {current_list_item_id, matching_list_item_id}
            else:
                people_names[current_list_item_name] = current_list_item_id

        list_model.same_name_items = list(same_name_items)

    def _remove_relationship_answers_for_list_item_id(
        self, list_item_id: str, answers: list
    ) -> None:
        for answer in answers:
            answers_to_keep = [
                value
                for value in answer.value
                if list_item_id not in {value["to_list_item_id"], value["list_item_id"]}
            ]
            answer.value = answers_to_keep
            self._answer_store.add_or_update(answer)

    def add_completed_location(self, location: LocationType) -> None:
        if not self._progress_store.is_routing_backwards:
            self._progress_store.add_completed_location(location)

    def remove_completed_location(self, location: LocationType) -> bool:
        return self._progress_store.remove_completed_location(location)

    def update_section_status(
        self, *, is_complete: bool, section_key: SectionKey
    ) -> bool:
        status = (
            CompletionStatus.COMPLETED if is_complete else CompletionStatus.IN_PROGRESS
        )
        return self._progress_store.update_section_status(status, section_key)

    def _update_answer(
        self,
        answer_id: str,
        list_item_id: str | None,
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

    def _capture_block_dependencies_for_list(self, list_name: str) -> None:
        """Captures a list of block ids that are dependents of the given list"""
        dependencies: set[Dependent] = self._schema.list_dependencies.get(
            list_name, set()
        )
        for dependent in dependencies:
            list_item_ids = self._get_list_item_ids_for_list_dependency(dependent)
            self._capture_block_dependent(dependent, list_item_ids)

    def _get_list_item_ids_for_list_dependency(
        self, dependency: Dependent
    ) -> list[str] | list[None]:
        if dependency.for_list:
            return self._list_store[dependency.for_list].items
        return [None]

    def _capture_block_dependent(
        self, dependent: Dependent, list_item_ids: Sequence[str] | Sequence[None]
    ) -> None:
        """
        The block_id is mapped to the section key. Dependents in a repeating section should be passed in with the list items
        for the repeating list for creating the section key.

        Blocks are captured regardless of whether they are complete. This avoids fetching the completed blocks
        multiples times, as you may have multiple dependencies for one block which may also apply to each item in the list.
        However, when updating the progress store, the block ids are checked to ensure they exist in the progress store.
        """
        for list_item_id in list_item_ids:
            if dependent.answer_id:
                self._answer_store.remove_answer(
                    dependent.answer_id, list_item_id=list_item_id
                )
            self.dependent_block_id_by_section_key[
                SectionKey(dependent.section_id, list_item_id)
            ].add(dependent.block_id)

    def _capture_section_dependencies_for_answer(self, answer_id: str) -> None:
        """Captures a unique list of section ids that are dependents of the provided answer id."""

        answer_id_section_dependents = (
            self._schema.when_rules_section_dependencies_by_answer
        )

        for section_id in answer_id_section_dependents.get(answer_id, {}):
            if repeating_list := self._schema.get_repeating_list_for_section(
                section_id
            ):
                for list_item_id in self._list_store[repeating_list].items:
                    self.dependent_sections.add(
                        DependentSection(section_id, list_item_id)
                    )
            else:
                self.dependent_sections.add(DependentSection(section_id))

    def _capture_section_dependencies_progress_value_source_for_section(
        self,
        section_id: str,
    ) -> None:
        """
        Captures a unique list of section ids that are dependents of the provided section, for progress value sources.
        """
        dependent_sections: Iterable = (
            self._schema.when_rules_section_dependencies_by_section_for_progress_value_source.get(
                section_id, set()
            )
        )
        self._update_section_dependencies(dependent_sections)

    def _capture_section_dependencies_progress_value_source_for_block(
        self, *, section_id: str, block_id: str
    ) -> None:
        """
        Captures a unique list of section ids that are dependents of the provided block, for progress value sources.
        """
        dependent_sections: Iterable = (
            self._schema.when_rules_block_dependencies_by_section_for_progress_value_source.get(
                section_id, {}
            ).get(
                block_id, set()
            )
        )
        self._update_section_dependencies(dependent_sections)

    def _update_section_dependencies(self, dependent_sections: Iterable) -> None:
        for section_id in dependent_sections:
            if repeating_list := self._schema.get_repeating_list_for_section(
                section_id
            ):
                for list_item_id in self._list_store[repeating_list].items:
                    self.dependent_sections.add(
                        DependentSection(section_id, list_item_id)
                    )
            else:
                self.dependent_sections.add(DependentSection(section_id))

    def update_progress_for_dependent_sections(self) -> None:
        """Removes dependent blocks from the progress store and updates the progress to IN_PROGRESS.
        Section progress is not updated for the current location as it is handled by `handle_post` on block handlers.
        """
        evaluated_dependents: list[tuple] = []

        chronological_dependents = self._get_chronological_section_dependents()

        for section in chronological_dependents:
            if (
                section.section_id,
                section.list_item_id,
            ) not in self.started_section_keys():
                continue

            if (
                section.section_id,
                section.list_item_id,
            ) not in evaluated_dependents:
                self._evaluate_dependents(
                    dependent_section=section, evaluated_dependents=evaluated_dependents
                )
                evaluated_dependents.append((section.section_id, section.list_item_id))

    def _evaluate_dependents(
        self,
        *,
        dependent_section: DependentSection,
        evaluated_dependents: list[tuple],
    ) -> None:
        is_path_complete = dependent_section.is_complete
        if is_path_complete is None:
            is_path_complete = self._router.is_path_complete(
                self._router.routing_path(dependent_section.section_key)
            )

        if self.update_section_status(
            is_complete=is_path_complete, section_key=dependent_section.section_key
        ):
            dependents_of_dependent: OrderedSet = (
                self._schema.when_rules_section_dependencies_by_section_for_progress_value_source.get(
                    dependent_section.section_id, OrderedSet()
                )
            )
            for dependent_section_id in dependents_of_dependent:
                if repeating_list := self._schema.get_repeating_list_for_section(
                    dependent_section_id
                ):
                    for item_id in self._list_store[repeating_list].items:
                        if (
                            dependent_section_id,
                            item_id,
                        ) not in evaluated_dependents:
                            self._evaluate_dependent_of_dependents(
                                dependent_section_id=dependent_section_id,
                                list_item_id=item_id,
                                evaluated_dependents=evaluated_dependents,
                            )
                elif (
                    dependent_section_id,
                    dependent_section.list_item_id,
                ) not in evaluated_dependents:
                    self._evaluate_dependent_of_dependents(
                        dependent_section_id=dependent_section_id,
                        evaluated_dependents=evaluated_dependents,
                    )

    def _evaluate_dependent_of_dependents(
        self,
        dependent_section_id: str,
        evaluated_dependents: list[tuple],
        list_item_id: str | None = None,
    ) -> None:
        self._evaluate_dependents(
            dependent_section=DependentSection(
                section_id=dependent_section_id,
                list_item_id=list_item_id,
            ),
            evaluated_dependents=evaluated_dependents,
        )
        evaluated_dependents.append((dependent_section_id, list_item_id))

    def remove_dependent_blocks_and_capture_dependent_sections(self) -> None:
        """Removes dependent blocks from the progress store."""

        for (
            section_key,
            blocks_to_remove,
        ) in self.dependent_block_id_by_section_key.items():
            if section_key not in self.started_section_keys():
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

            if blocks_removed:
                self._capture_dependent_section(section_key)

    def _capture_dependent_section(self, section_key: SectionKey) -> None:
        """
        Since this section key will be marked as incomplete, any `DependentSection` with is_complete as `None`
        can be removed as we do not need to re-evaluate progress as we already know the section would be incomplete.
        """
        dependent = DependentSection(**section_key.to_dict())
        if dependent in self.dependent_sections:
            self.dependent_sections.remove(dependent)

        self.dependent_sections.add(
            DependentSection(**section_key.to_dict(), is_complete=False)
        )

    def started_section_keys(
        self, section_ids: Iterable[str] | None = None
    ) -> list[SectionKey]:
        return self._progress_store.started_section_keys(section_ids)

    def _get_chronological_section_dependents(self) -> list:
        sections = list(self._schema.get_section_ids())
        return sorted(
            self.dependent_sections, key=lambda x: sections.index(x.section_id)
        )

    def set_supplementary_data(self, to_set: MutableMapping) -> None:
        """
        Used to set or update the supplementary data whenever the sds endpoint is called
        (Which should be once per session, but only if the sds_dataset_id has changed)

        this updates ListStore to add/update any lists for supplementary data and stores the
        identifier -> list_item_id mappings in the supplementary data store to use in the payload at the end
        """
        list_mappings: dict[str, list[SupplementaryDataListMapping]] = {}
        modified_lists: set[str] = set()

        if self._supplementary_data_store.list_mappings:
            modified_lists |= self._remove_outdated_supplementary_lists_and_answers(
                new_data=to_set
            )

        for list_name, list_data in to_set.get("items", {}).items():
            mappings, lists = self._create_supplementary_list(
                list_name=list_name, list_data=list_data
            )
            list_mappings[list_name] = mappings
            modified_lists |= lists

        for list_name in modified_lists:
            self.capture_dependencies_for_list_change(list_name)

        self._supplementary_data_store = SupplementaryDataStore(
            supplementary_data=to_set, list_mappings=list_mappings
        )

    def _create_supplementary_list(
        self, *, list_name: str, list_data: Sequence[dict]
    ) -> tuple[list[SupplementaryDataListMapping], set[str]]:
        """
        Creates or updates a list in ListStore based off supplementary data
        returns the identifier -> list_item_id mappings used and the lists that were modified in the process
        """
        list_mappings: list[SupplementaryDataListMapping] = []
        modified_lists: set[str] = set()
        for list_item in list_data:
            identifier = list_item["identifier"]
            # if any pre-existing supplementary data already has a mapping for this list item
            # then its already in the list store and doesn't require adding
            if not (
                list_item_id := self._supplementary_data_store.list_lookup.get(
                    list_name, {}
                ).get(identifier)
            ):
                list_item_id = self.add_list_item(list_name)
                modified_lists.add(list_name)
            list_mappings.append(
                SupplementaryDataListMapping(
                    identifier=identifier, list_item_id=list_item_id
                )
            )
        return list_mappings, modified_lists

    def _remove_outdated_supplementary_lists_and_answers(
        self, new_data: MutableMapping
    ) -> set[str]:
        """
        In the case that existing supplementary data is being replaced with new data: any list items in the old data
        but not the new data are removed from the list store and related answers are deleted
        :param new_data - the new supplementary data for comparison
        :return: any lists that were modified by the change in supplementary data
        """
        modified_lists: set[str] = set()
        for (
            list_name,
            mappings,
        ) in self._supplementary_data_store.list_lookup.items():
            if list_name in new_data.get("items", {}):
                new_identifiers = [
                    item["identifier"] for item in new_data["items"][list_name]
                ]
                for identifier, list_item_id in mappings.items():
                    if identifier not in new_identifiers:
                        modified_lists.add(list_name)
                        self.remove_list_item_data(list_name, list_item_id)
            else:
                self.remove_list_data(list_name)
        return modified_lists


class QuestionnaireStoreUpdater(QuestionnaireStoreUpdaterBase):
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

    def _capture_dependent_section(self, section_key: SectionKey) -> None:
        """Only capture the dependent section if it is not the current one"""
        if section_key != self._current_location.section_key:
            super()._capture_dependent_section(section_key)
