# pylint: disable=too-many-lines
from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass
from functools import cached_property
from typing import Any, Generator, Iterable, Mapping, Sequence, TypeAlias

from flask_babel import force_locale
from ordered_set import OrderedSet
from werkzeug.datastructures import ImmutableDict, MultiDict

from app.data_models.answer import Answer
from app.forms import error_messages
from app.questionnaire.rules.operator import OPERATION_MAPPING
from app.questionnaire.schema_utils import get_answers_from_question
from app.utilities.make_immutable import make_immutable
from app.utilities.mappings import get_flattened_mapping_values, get_mappings_with_key

DEFAULT_LANGUAGE_CODE = "en"

LIST_COLLECTORS_WITH_REPEATING_BLOCKS = {"ListCollector", "ListCollectorContent"}

LIST_COLLECTOR_CHILDREN = [
    "ListAddQuestion",
    "ListEditQuestion",
    "ListRemoveQuestion",
    "PrimaryPersonListAddOrEditQuestion",
    "ListRepeatingQuestion",
]

RELATIONSHIP_CHILDREN = ["UnrelatedQuestion"]

QuestionSchemaType = Mapping

DependencyDictType: TypeAlias = dict[str, OrderedSet[str]]

TRANSFORMS_REQUIRING_ROUTING_PATH = {"first_non_empty_item"}


class InvalidSchemaConfigurationException(Exception):
    pass


@dataclass(frozen=True)
class AnswerDependent:
    """Represents a dependent belonging to some answer.

    The dependent can be a reference to another answer, or just the parent block of the answer.
    If the dependent has an answer_id, then the dependent answer is removed
    when the answer this dependents upon is changed.

    An answer can have zero or more dependents.
    """

    section_id: str
    block_id: str
    for_list: str | None = None
    answer_id: str | None = None


class QuestionnaireSchema:  # pylint: disable=too-many-public-methods
    def __init__(
        self, questionnaire_json: Mapping, language_code: str = DEFAULT_LANGUAGE_CODE
    ):
        self._parent_id_map: dict[str, str] = {}
        self._list_name_to_section_map: dict[str, list[str]] = {}
        self._answer_dependencies_map: dict[str, set[AnswerDependent]] = defaultdict(
            set
        )
        self._when_rules_section_dependencies_by_section: dict[str, set[str]] = {}
        self._when_rules_section_dependencies_by_section_for_progress_value_source: defaultdict[
            str, OrderedSet[str]
        ] = defaultdict(
            OrderedSet
        )
        self._when_rules_block_dependencies_by_section_for_progress_value_source: defaultdict[
            str, DependencyDictType
        ] = defaultdict(
            lambda: defaultdict(OrderedSet)
        )
        self.calculated_summary_section_dependencies_by_block: dict[
            str, DependencyDictType
        ] = defaultdict(lambda: defaultdict(OrderedSet))
        self._when_rules_section_dependencies_by_answer: dict[
            str, set[str]
        ] = defaultdict(set)
        self._placeholder_transform_section_dependencies_by_block: dict[
            str, dict[str, set[str]]
        ] = defaultdict(lambda: defaultdict(set))
        self._language_code = language_code
        self._questionnaire_json = questionnaire_json
        self._list_names_by_list_repeating_block_id: dict[str, str] = {}
        self._repeating_block_answer_ids: set[str] = set()
        self.dynamic_answers_parent_block_ids: set[str] = set()

        # The ordering here is required as they depend on each other.
        self._sections_by_id = self._get_sections_by_id()
        self._groups_by_id = self._get_groups_by_id()
        self._blocks_by_id = self._get_blocks_by_id()
        self._questions_by_id = self._get_questions_by_id()
        self._answers_by_id = self._get_answers_by_id()
        self._dynamic_answer_ids: set[str] = set()
        self._list_dependent_block_additional_dependencies: dict[str, set[str]] = {}

        # Post schema parsing.
        self._populate_answer_dependencies()
        self._populate_when_rules_section_dependencies()
        self._populate_calculated_summary_section_dependencies()
        self._populate_placeholder_transform_section_dependencies()

    @property
    def placeholder_transform_section_dependencies_by_block(
        self,
    ) -> dict[str, dict[str, set[str]]]:
        return self._placeholder_transform_section_dependencies_by_block

    @cached_property
    def answer_dependencies(self) -> ImmutableDict[str, set[AnswerDependent]]:
        return ImmutableDict(self._answer_dependencies_map)

    @cached_property
    def when_rules_section_dependencies_by_section(
        self,
    ) -> ImmutableDict[str, set[str]]:
        return ImmutableDict(self._when_rules_section_dependencies_by_section)

    @cached_property
    def when_rules_section_dependencies_for_progress(
        self,
    ) -> ImmutableDict[str, set[str]]:
        """
        This method flips the dependencies that were captured for progress value sources so that they can be
        evaluated properly for when rules, this is because for when rules we need to check for dependencies in
        previous sections, whereas for progress we are checking for dependent blocks/sections in "future" sections
        """
        when_rules_section_dependencies_for_progress = defaultdict(set)
        for (
            section,
            dependent,
        ) in (
            self._when_rules_block_dependencies_by_section_for_progress_value_source.items()
        ):
            section_dependents = get_flattened_mapping_values(dependent)
            for dependent_section in section_dependents:
                when_rules_section_dependencies_for_progress[dependent_section].add(
                    section
                )

        for (
            section,
            dependents,
        ) in (
            self._when_rules_section_dependencies_by_section_for_progress_value_source.items()
        ):
            for dependent_section in dependents:
                when_rules_section_dependencies_for_progress[dependent_section].add(
                    section
                )
        return ImmutableDict(when_rules_section_dependencies_for_progress)

    @cached_property
    def when_rules_section_dependencies_by_section_for_progress_value_source(
        self,
    ) -> ImmutableDict[str, OrderedSet[str]]:
        return ImmutableDict(
            self._when_rules_section_dependencies_by_section_for_progress_value_source
        )

    @cached_property
    def when_rules_block_dependencies_by_section_for_progress_value_source(
        self,
    ) -> ImmutableDict[str, DependencyDictType]:
        return ImmutableDict(
            self._when_rules_block_dependencies_by_section_for_progress_value_source
        )

    @cached_property
    def when_rules_section_dependencies_by_answer(self) -> ImmutableDict[str, set[str]]:
        return ImmutableDict(self._when_rules_section_dependencies_by_answer)

    @cached_property
    def language_code(self) -> str:
        return self._language_code

    @cached_property
    def error_messages(self) -> Any:
        return self.serialize(self._get_error_messages())

    @cached_property
    def json(self) -> Any:
        return self.serialize(self._questionnaire_json)

    @cached_property
    def survey(self) -> str | None:
        survey: str | None = self.json.get("survey")
        return survey

    @cached_property
    def form_type(self) -> str | None:
        form_type: str | None = self.json.get("form_type")
        return form_type

    @cached_property
    def region_code(self) -> str | None:
        region_code: str | None = self.json.get("region_code")
        return region_code

    @cached_property
    def preview_enabled(self) -> bool:
        preview_enabled: bool = self.json.get("preview_questions", False)
        return preview_enabled

    @cached_property
    def parent_id_map(self) -> Any:
        return self.serialize(self._parent_id_map)

    @classmethod
    def serialize(cls, data: Any) -> Any:
        return make_immutable(data)

    @classmethod
    def get_mutable_deepcopy(cls, data: Any) -> Any:
        if isinstance(data, tuple):
            return list((cls.get_mutable_deepcopy(item) for item in data))
        if isinstance(data, ImmutableDict):
            key_value_tuples = {k: cls.get_mutable_deepcopy(v) for k, v in data.items()}
            return dict(key_value_tuples)
        return deepcopy(data)

    @cached_property
    def _flow(self) -> ImmutableDict:
        questionnaire_flow: ImmutableDict = self.json["questionnaire_flow"]
        return questionnaire_flow

    @cached_property
    def flow_options(self) -> ImmutableDict:
        options: ImmutableDict = self._flow["options"]
        return options

    @cached_property
    def is_flow_hub(self) -> bool:
        return bool(self._flow["type"] == "Hub")

    @cached_property
    def is_flow_linear(self) -> bool:
        return bool(self._flow["type"] == "Linear")

    @cached_property
    def is_view_submitted_response_enabled(self) -> bool:
        schema: Mapping = self.get_post_submission()
        is_enabled: bool = schema.get("view_response", False)
        return is_enabled

    @cached_property
    def list_names_by_list_repeating_block_id(self) -> ImmutableDict[str, str]:
        return ImmutableDict(self._list_names_by_list_repeating_block_id)

    @cached_property
    def list_collector_repeating_block_ids(self) -> list[str]:
        return list(self._list_names_by_list_repeating_block_id.keys())

    def get_all_when_rules_section_dependencies_for_section(
        self, section_id: str
    ) -> set[str]:
        all_section_dependencies = self.when_rules_section_dependencies_by_section.get(
            section_id, set()
        )

        if progress_dependencies := self.when_rules_section_dependencies_for_progress.get(
            section_id
        ):
            all_section_dependencies.update(progress_dependencies)

        return all_section_dependencies

    def _get_sections_by_id(self) -> dict[str, ImmutableDict]:
        return {
            section["id"]: section
            for section in self.json.get("sections", ImmutableDict({}))
        }

    def _get_groups_by_id(self) -> dict[str, ImmutableDict]:
        groups_by_id: dict[str, ImmutableDict] = {}

        for section in self._sections_by_id.values():
            for group in section["groups"]:
                group_id = group["id"]
                groups_by_id[group_id] = group
                self._parent_id_map[group_id] = section["id"]

        return groups_by_id

    def _get_blocks_by_id(self) -> dict[str, ImmutableDict]:
        blocks: dict[str, ImmutableDict] = {}

        for group in self._groups_by_id.values():
            for block in group["blocks"]:
                block_id = block["id"]
                self._parent_id_map[block_id] = group["id"]

                blocks[block_id] = block
                if block["type"] in {
                    "ListCollector",
                    "ListCollectorContent",
                    "PrimaryPersonListCollector",
                    "RelationshipCollector",
                }:
                    for nested_block_name in [
                        "add_block",
                        "edit_block",
                        "remove_block",
                        "add_or_edit_block",
                        "unrelated_block",
                    ]:
                        if block.get(nested_block_name):
                            nested_block = block[nested_block_name]
                            nested_block_id = nested_block["id"]
                            blocks[nested_block_id] = nested_block
                            self._parent_id_map[nested_block_id] = block_id
                    if repeating_blocks := block.get("repeating_blocks"):
                        for repeating_block in repeating_blocks:
                            repeating_block_id = repeating_block["id"]
                            blocks[repeating_block_id] = repeating_block
                            self._parent_id_map[repeating_block_id] = block_id
                            self._list_names_by_list_repeating_block_id[
                                repeating_block_id
                            ] = block["for_list"]

        return blocks

    def _get_questions_by_id(self) -> dict[str, list[ImmutableDict]]:
        questions_by_id = defaultdict(list)

        for block in self._blocks_by_id.values():
            questions = self.get_all_questions_for_block(block)
            for question in questions:
                question_id = question["id"]
                questions_by_id[question_id].append(question)
                self._parent_id_map[question_id] = block["id"]

        return questions_by_id

    def _get_answers_by_id(self) -> dict[str, list[ImmutableDict]]:
        answers_by_id = defaultdict(list)

        for question in self._get_flattened_questions():
            question_id = question["id"]
            is_for_repeating_block = (
                self._parent_id_map[question_id]
                in self.list_collector_repeating_block_ids
            )

            for answer in get_answers_from_question(question):
                answer_id = answer["id"]
                self._parent_id_map[answer_id] = question_id
                if is_for_repeating_block:
                    self._repeating_block_answer_ids.add(answer_id)

                answers_by_id[answer_id].append(answer)
                for option in answer.get("options", []):
                    detail_answer = option.get("detail_answer")
                    if detail_answer:
                        detail_answer_id = detail_answer["id"]
                        answers_by_id[detail_answer_id].append(detail_answer)
                        self._parent_id_map[detail_answer_id] = question_id

        return answers_by_id

    def _populate_answer_dependencies(self) -> None:
        for block in self.get_blocks():
            if block["type"] in {"CalculatedSummary", "GrandCalculatedSummary"}:
                self._update_answer_dependencies_for_summary(block)
                continue

            if block["type"] == "ListCollector" and block.get("repeating_blocks"):
                self._update_dependencies_for_list_repeating_blocks(block)

            for question in self.get_all_questions_for_block(block):
                self.update_dependencies_for_dynamic_answers(
                    question=question, block_id=block["id"]
                )

                if question["type"] == "Calculated":
                    self._update_answer_dependencies_for_calculations(
                        question["calculations"], block_id=block["id"]
                    )
                    continue

                for answer in question.get("answers", []):
                    self._update_answer_dependencies_for_answer(
                        answer, block_id=block["id"]
                    )
                    for option in answer.get("options", []):
                        if "detail_answer" in option:
                            self._update_answer_dependencies_for_answer(
                                option["detail_answer"], block_id=block["id"]
                            )

    def _update_dependencies_for_list_repeating_blocks(
        self, list_collector_block: ImmutableDict
    ) -> None:
        """Blocks depending on repeating questions may need to depend on adding/removing items from the parent list collector, so update the map"""
        list_block_dependencies: set[str] = set()
        for child in ("add_block", "remove_block"):
            if child_block := list_collector_block.get(child):
                list_block_dependencies.update(
                    self.get_answer_ids_for_block(child_block["id"])
                )

        if list_block_dependencies:
            for repeating_block in list_collector_block["repeating_blocks"]:
                self._list_dependent_block_additional_dependencies[
                    repeating_block["id"]
                ] = list_block_dependencies

    def _update_answer_dependencies_for_summary(self, block: ImmutableDict) -> None:
        if block["type"] == "CalculatedSummary":
            self._update_answer_dependencies_for_calculated_summary_dependency(
                calculated_summary_block=block, dependent_block=block
            )
        elif block["type"] == "GrandCalculatedSummary":
            self._update_answer_dependencies_for_grand_calculated_summary(block)

    def _update_answer_dependencies_for_calculated_summary_dependency(
        self, *, calculated_summary_block: ImmutableDict, dependent_block: ImmutableDict
    ) -> None:
        """
        update all calculated summary answers to be dependencies of the dependent block

        in the case that one of the calculated summary answers is dynamic/repeating, so has multiple answers for a particular list
        the calculated summary block needs to depend on the `remove_block` and `add_block` for the list
        so that adding/removing items requires re-confirming the calculated summary
        """
        calculated_summary_answer_ids = get_calculated_summary_answer_ids(
            calculated_summary_block
        )
        answer_dependent = self._get_answer_dependent_for_block_id(
            block_id=dependent_block["id"]
        )
        for answer_id in calculated_summary_answer_ids:
            if answer_id in [
                *self._dynamic_answer_ids,
                *self._repeating_block_answer_ids,
            ]:
                # Type ignore: answer_id is valid so block must exist
                block_id: str = self.get_block_for_answer_id(answer_id)["id"]  # type: ignore
                if block_id in self._list_dependent_block_additional_dependencies:
                    for (
                        list_block_id
                    ) in self._list_dependent_block_additional_dependencies[block_id]:
                        self._answer_dependencies_map[list_block_id].add(
                            answer_dependent
                        )
            self._answer_dependencies_map[answer_id].add(answer_dependent)

    def _update_answer_dependencies_for_grand_calculated_summary(
        self, grand_calculated_summary_block: ImmutableDict
    ) -> None:
        grand_calculated_summary_calculated_summary_ids = (
            get_calculation_block_ids_for_grand_calculated_summary(
                grand_calculated_summary_block
            )
        )
        for calculated_summary_id in grand_calculated_summary_calculated_summary_ids:
            # Type ignore: safe to assume block exists
            calculated_summary_block: ImmutableDict = self.get_block(calculated_summary_id)  # type: ignore
            self._update_answer_dependencies_for_calculated_summary_dependency(
                calculated_summary_block=calculated_summary_block,
                dependent_block=grand_calculated_summary_block,
            )

    def _update_answer_dependencies_for_calculations(
        self, calculations: tuple[ImmutableDict, ...], *, block_id: str
    ) -> None:
        for calculation in calculations:
            if source_answer_id := calculation.get("answer_id"):
                dependents = {
                    self._get_answer_dependent_for_block_id(
                        block_id=self.get_block_for_answer_id(answer_id)["id"]  # type: ignore
                    )
                    for answer_id in calculation["answers_to_calculate"]
                }
                self._answer_dependencies_map[source_answer_id] |= dependents

            elif isinstance(calculation.get("value"), dict):
                self._update_answer_dependencies_for_value_source(
                    calculation["value"],
                    block_id=block_id,
                )

    def _update_answer_dependencies_for_answer(
        self, answer: Mapping, *, block_id: str
    ) -> None:
        for key in ["minimum", "maximum"]:
            value = answer.get(key, {}).get("value")
            if isinstance(value, dict):
                self._update_answer_dependencies_for_value_source(
                    value,
                    block_id=block_id,
                )

        if dynamic_options_values := answer.get("dynamic_options", {}).get("values"):
            self._update_answer_dependencies_for_dynamic_options(
                dynamic_options_values, block_id=block_id, answer_id=answer["id"]
            )

    def _update_answer_dependencies_for_dynamic_options(
        self,
        dynamic_options_values: Mapping,
        *,
        block_id: str,
        answer_id: str,
    ) -> None:
        value_sources = get_mappings_with_key("source", dynamic_options_values)
        for value_source in value_sources:
            self._update_answer_dependencies_for_value_source(
                value_source, block_id=block_id, answer_id=answer_id
            )

    def _update_answer_dependencies_for_value_source(
        self,
        value_source: Mapping,
        *,
        block_id: str,
        answer_id: str | None = None,
    ) -> None:
        if value_source["source"] == "answers":
            self._answer_dependencies_map[value_source["identifier"]] |= {
                self._get_answer_dependent_for_block_id(
                    block_id=block_id, answer_id=answer_id
                )
            }
        if value_source["source"] == "calculated_summary":
            identifier = value_source["identifier"]
            if calculated_summary_block := self.get_block(identifier):
                answer_ids_for_block = get_calculated_summary_answer_ids(
                    calculated_summary_block
                )

                for answer_id_for_block in answer_ids_for_block:
                    self._answer_dependencies_map[answer_id_for_block] |= {
                        self._get_answer_dependent_for_block_id(
                            block_id=block_id, answer_id=answer_id
                        )
                    }
        if value_source["source"] == "list":
            self._update_answer_dependencies_for_list_source(
                block_id=block_id, list_name=value_source["identifier"]
            )

    def _update_answer_dependencies_for_list_source(
        self, *, block_id: str, list_name: str
    ) -> None:
        """Updates dependencies for a block depending on a list collector

        This method also stores a map of { block_depending_on_list_source -> {add_block, remove_block} }, because:
        blocks like dynamic_answers, don't directly need to depend on the add_block/remove_block,
        but a block depending on the dynamic answers might (such as a calculated summary)
        """
        # Type ignore: section will always exist at this point, same with optional returns below
        section: ImmutableDict = self.get_section_for_block_id(block_id)  # type: ignore
        list_collector: ImmutableDict = self.get_list_collector_for_list(  # type: ignore
            section=section,
            for_list=list_name,
        )

        add_block_question = self.get_add_block_for_list_collector(  # type: ignore
            list_collector["id"]
        )["question"]
        answer_ids_for_block = list(
            self.get_answers_for_question_by_id(add_block_question)
        )
        for block_answer_id in answer_ids_for_block:
            self._answer_dependencies_map[block_answer_id] |= {
                self._get_answer_dependent_for_block_id(
                    block_id=block_id, for_list=list_name
                )
                if self.is_block_in_repeating_section(block_id)
                # non-repeating blocks such as dynamic-answers could depend on the list
                else self._get_answer_dependent_for_block_id(block_id=block_id)
            }
        self._list_dependent_block_additional_dependencies[block_id] = set(
            answer_ids_for_block
        )
        # removing an item from a list will require any dependent calculated summaries to be re-confirmed, so cache dependencies
        if remove_block_id := self.get_remove_block_id_for_list(list_name):
            self._list_dependent_block_additional_dependencies[block_id].update(
                self.get_answer_ids_for_block(remove_block_id)
            )

    def _get_answer_dependent_for_block_id(
        self,
        *,
        block_id: str,
        answer_id: str | None = None,
        for_list: str | None = None,
    ) -> AnswerDependent:
        section_id: str = self.get_section_id_for_block_id(block_id)  # type: ignore
        if not for_list:
            for_list = self.get_repeating_list_for_section(section_id)

        return AnswerDependent(
            block_id=block_id,
            section_id=section_id,
            for_list=for_list,
            answer_id=answer_id,
        )

    def _get_flattened_questions(self) -> list[ImmutableDict]:
        return [
            question
            for questions in self._questions_by_id.values()
            for question in questions
        ]

    def get_section_ids_required_for_hub(self) -> tuple[str, ...]:
        return self.flow_options.get("required_completed_sections", tuple())

    def get_summary_options(self) -> ImmutableDict[str, bool]:
        return self.flow_options.get("summary", ImmutableDict({}))

    def get_sections(self) -> Iterable[ImmutableDict]:
        return self._sections_by_id.values()

    def get_section_ids(self) -> Iterable[str]:
        return self._sections_by_id.keys()

    def get_section(self, section_id: str) -> ImmutableDict | None:
        return self._sections_by_id.get(section_id)

    def get_section_ids_dependent_on_list(self, list_name: str) -> list[str]:
        try:
            return self._list_name_to_section_map[list_name]
        except KeyError:
            section_ids = self._section_ids_associated_to_list_name(list_name)
            self._list_name_to_section_map[list_name] = section_ids
            return section_ids

    def get_submission(self) -> ImmutableDict:
        schema: ImmutableDict = self.json.get("submission", ImmutableDict({}))
        return schema

    def get_post_submission(self) -> ImmutableDict:
        schema: ImmutableDict = self.json.get("post_submission", ImmutableDict({}))
        return schema

    def _is_list_name_in_rule(
        self, when_rule: Mapping[str, list], list_name: str
    ) -> bool:
        if not QuestionnaireSchema.has_operator(when_rule):
            return False

        operands = self.get_operands(when_rule)

        for operand in operands:
            if not isinstance(operand, Mapping):
                continue
            if "source" in operand:
                return bool(
                    operand.get("source") == "list"
                    and operand.get("identifier") == list_name
                )

            # Nested rules
            if QuestionnaireSchema.has_operator(operand):
                return self._is_list_name_in_rule(operand, list_name)

        return False

    @staticmethod
    def get_operands(rules: Mapping) -> Sequence:
        operator = next(iter(rules))
        operands: Sequence = rules[operator]
        return operands

    def _section_ids_associated_to_list_name(self, list_name: str) -> list[str]:
        section_ids: list[str] = []

        for section in self.get_sections():
            ignore_keys = ["question_variants", "content_variants"]
            when_rules = self.get_values_for_key(section, "when", ignore_keys)

            rule: Mapping = next(when_rules, {})
            if self._is_list_name_in_rule(rule, list_name):
                section_ids.append(section["id"])
        return section_ids

    @staticmethod
    def get_blocks_for_section(
        section: Mapping,
    ) -> Generator[ImmutableDict, None, None]:
        return (block for group in section["groups"] for block in group["blocks"])

    @classmethod
    def get_driving_question_for_list(
        cls, section: Mapping, list_name: str
    ) -> ImmutableDict | None:
        for block in cls.get_blocks_for_section(section):
            if (
                block["type"] == "ListCollectorDrivingQuestion"
                and list_name == block["for_list"]
            ):
                return block

    def get_remove_block_id_for_list(self, list_name: str) -> str | None:
        for block in self.get_blocks():
            if (
                is_list_collector_block_editable(block)
                and block["for_list"] == list_name
            ):
                remove_block_id: str = block["remove_block"]["id"]
                return remove_block_id

    def get_individual_response_list(self) -> str | None:
        list_name: str | None = self.json.get("individual_response", {}).get("for_list")
        return list_name

    def get_individual_response_show_on_hub(self) -> bool:
        show_on_hub: bool = self.json.get("individual_response", {}).get(
            "show_on_hub", True
        )
        return show_on_hub

    def get_individual_response_individual_section_id(self) -> str | None:
        section_id: str | None = self._questionnaire_json.get(
            "individual_response", {}
        ).get("individual_section_id")
        return section_id

    def get_title_for_section(self, section_id: str) -> str | None:
        if section := self.get_section(section_id):
            return section.get("title")

    def get_show_on_hub_for_section(self, section_id: str) -> bool | None:
        if section := self.get_section(section_id):
            return section.get("show_on_hub", True)

    def get_summary_for_section(self, section_id: str) -> ImmutableDict | None:
        if section := self.get_section(section_id):
            return section.get("summary")

    def get_summary_title_for_section(self, section_id: str) -> str | None:
        if summary := self.get_summary_for_section(section_id):
            return summary.get("title")

    def show_summary_on_completion_for_section(self, section_id: str) -> bool | None:
        if summary := self.get_summary_for_section(section_id):
            return summary.get("show_on_completion", False)

    def get_repeat_for_section(self, section_id: str) -> ImmutableDict | None:
        if section := self.get_section(section_id):
            return section.get("repeat")

    def get_repeating_list_for_section(self, section_id: str) -> str | None:
        if repeat := self.get_repeat_for_section(section_id):
            return repeat.get("for_list")

    def get_repeating_title_for_section(self, section_id: str) -> ImmutableDict | None:
        if repeat := self.get_repeat_for_section(section_id):
            title: ImmutableDict = repeat["title"]
            return title

    def get_repeating_page_title_for_section(self, section_id: str) -> str | None:
        if repeat := self.get_repeat_for_section(section_id):
            return repeat.get("page_title")

    def get_custom_page_title_for_section(self, section_id: str) -> str | None:
        if summary := self.get_summary_for_section(section_id):
            return summary.get("page_title")

    def get_section_for_block_id(self, block_id: str) -> ImmutableDict | None:
        block = self.get_block(block_id)

        if (
            block
            and block.get("type") in LIST_COLLECTOR_CHILDREN + RELATIONSHIP_CHILDREN
        ):
            section_id = self._get_parent_section_id_for_block(block_id)
        else:
            group_id = self._parent_id_map[block_id]
            section_id = self._parent_id_map[group_id]

        return self.get_section(section_id)

    def get_section_id_for_block_id(self, block_id: str) -> str | None:
        if section := self.get_section_for_block_id(block_id):
            section_id: str = section["id"]
            return section_id

    def get_groups(self) -> Iterable[ImmutableDict]:
        return self._groups_by_id.values()

    def get_group(self, group_id: str) -> ImmutableDict | None:
        return self._groups_by_id.get(group_id)

    def get_group_for_block_id(self, block_id: str) -> ImmutableDict | None:
        return self._group_for_block(block_id)

    def get_first_block_id_for_group(self, group_id: str) -> str | None:
        if group := self.get_group(group_id):
            block_id: str = group["blocks"][0]["id"]
            return block_id

    def get_first_block_id_for_section(self, section_id: str) -> str | None:
        if section := self.get_section(section_id):
            group_id: str = section["groups"][0]["id"]
            return self.get_first_block_id_for_group(group_id)

    def get_blocks(self) -> Iterable[ImmutableDict]:
        return self._blocks_by_id.values()

    def get_block(self, block_id: str) -> ImmutableDict | None:
        return self._blocks_by_id.get(block_id)

    def is_block_valid(self, block_id: str) -> bool:
        return bool(self.get_block(block_id))

    def get_block_for_answer_id(self, answer_id: str) -> ImmutableDict | None:
        return self._block_for_answer(answer_id)

    def is_block_in_repeating_section(self, block_id: str) -> bool | None:
        if section_id := self.get_section_id_for_block_id(block_id=block_id):
            return bool(self.get_repeating_list_for_section(section_id))

    def is_answer_in_list_collector_block(self, answer_id: str) -> bool | None:
        if block := self.get_block_for_answer_id(answer_id):
            return self.is_list_block_type(block["type"])

    def is_answer_in_repeating_section(self, answer_id: str) -> bool | None:
        if block := self.get_block_for_answer_id(answer_id):
            return self.is_block_in_repeating_section(block_id=block["id"])

    def is_answer_dynamic(self, answer_id: str) -> bool:
        return answer_id in self._dynamic_answer_ids

    def is_answer_in_list_collector_repeating_block(self, answer_id: str) -> bool:
        return answer_id in self._repeating_block_answer_ids

    def get_list_name_for_dynamic_answer(self, block_id: str) -> str:
        # type ignore block always exists at this point
        return self.get_block(block_id)["question"]["dynamic_answers"]["values"]["identifier"]  # type: ignore

    def is_repeating_answer(
        self,
        answer_id: str,
    ) -> bool:
        return bool(
            self.is_answer_in_list_collector_block(answer_id)
            or self.is_answer_in_repeating_section(answer_id)
            or self.is_answer_dynamic(answer_id)
        )

    def get_answers_by_answer_id(self, answer_id: str) -> list[ImmutableDict]:
        """Return answers matching answer id, including all matching answers inside
        variants
        """
        answers: list[ImmutableDict] = self._answers_by_id.get(answer_id, [])
        return answers

    def get_default_answer(self, answer_id: str) -> Answer | None:
        if answer_schemas := self.get_answers_by_answer_id(answer_id):
            first_answer_schema = answer_schemas[0]
            try:
                return Answer(first_answer_schema["id"], first_answer_schema["default"])
            except (IndexError, KeyError, TypeError):
                return None
        return None

    def get_add_block_for_list_collector(
        self, list_collector_id: str
    ) -> ImmutableDict | None:
        if list_collector := self.get_block(list_collector_id):
            add_block_map = {
                "ListCollector": "add_block",
                "PrimaryPersonListCollector": "add_or_edit_block",
            }
            add_block: ImmutableDict = list_collector[
                add_block_map[list_collector["type"]]
            ]
            return add_block

    def get_edit_block_for_list_collector(
        self, list_collector_id: str
    ) -> ImmutableDict | None:
        # Type ignore: for any valid list collector id, list collector block will always exist
        return self.get_block(list_collector_id).get("edit_block")  # type: ignore

    def get_repeating_blocks_for_list_collector(
        self, list_collector_id: str
    ) -> list[ImmutableDict] | None:
        if list_collector := self.get_block(list_collector_id):
            return list_collector.get("repeating_blocks", [])

    def get_answer_ids_for_list_items(self, list_collector_id: str) -> list[str]:
        """
        Get answer ids used to add items to a list, including any repeating block answers if any exist.
        """
        answer_ids = []
        if add_block := self.get_add_block_for_list_collector(list_collector_id):
            answer_ids.extend(self.get_answer_ids_for_block(add_block["id"]))
        if repeating_blocks := self.get_repeating_blocks_for_list_collector(
            list_collector_id
        ):
            for repeating_block in repeating_blocks:
                answer_ids.extend(self.get_answer_ids_for_block(repeating_block["id"]))
        return answer_ids

    def get_questions(self, question_id: str) -> list[ImmutableDict] | None:
        """Return a list of questions matching some question id
        This includes all questions inside variants
        """
        return self._questions_by_id.get(question_id)

    @staticmethod
    def get_list_collectors_for_list(
        section: Mapping, for_list: str, primary: bool = False
    ) -> Generator[ImmutableDict, None, None]:
        collector_type = (
            {"PrimaryPersonListCollector"}
            if primary
            else {"ListCollectorContent", "ListCollector"}
        )

        return (
            block
            for block in QuestionnaireSchema.get_blocks_for_section(section)
            if block["type"] in collector_type and block["for_list"] == for_list
        )

    @staticmethod
    def get_list_collector_for_list(
        section: Mapping, for_list: str, primary: bool = False
    ) -> ImmutableDict | None:
        try:
            return next(
                QuestionnaireSchema.get_list_collectors_for_list(
                    section, for_list, primary
                )
            )
        except StopIteration:
            return None

    @classmethod
    def get_answers_for_question_by_id(
        cls, question: QuestionSchemaType
    ) -> dict[str, dict]:
        answers: dict[str, dict] = {}

        for answer in get_answers_from_question(question):
            answers[answer["id"]] = answer
            for option in answer.get("options", {}):
                if "detail_answer" in option:
                    answers[option["detail_answer"]["id"]] = option["detail_answer"]

        return answers

    @classmethod
    def get_answer_ids_for_question(cls, question: QuestionSchemaType) -> list[str]:
        return list(cls.get_answers_for_question_by_id(question).keys())

    def get_first_answer_id_for_block(self, block_id: str) -> str:
        answer_ids = self.get_answer_ids_for_block(block_id)
        return answer_ids[0]

    def get_answer_format_for_calculated_summary(
        self, calculated_summary_block_id: str
    ) -> dict:
        """
        Given a calculated summary block id, find the format of the total by using the first answer
        """
        # Type ignore: the block will exist for any valid calculated summary id
        calculated_summary_block: ImmutableDict = self.get_block(calculated_summary_block_id)  # type: ignore
        first_answer_id = get_calculated_summary_answer_ids(calculated_summary_block)[0]
        first_answer = self.get_answers_by_answer_id(first_answer_id)[0]
        return {
            "type": first_answer["type"].lower(),
            "unit": first_answer.get("unit"),
            "unit_length": first_answer.get("unit_length"),
            "currency": first_answer.get("currency"),
        }

    def get_answer_ids_for_block(self, block_id: str) -> list[str]:
        if block := self.get_block(block_id):
            if block.get("question"):
                return self.get_answer_ids_for_question(block["question"])
            if block.get("question_variants"):
                return self.get_answer_ids_for_question(
                    block["question_variants"][0]["question"]
                )
        return []

    def get_relationship_collectors(self) -> list[ImmutableDict]:
        return [
            block
            for block in self.get_blocks()
            if block["type"] == "RelationshipCollector"
        ]

    def get_relationship_collectors_by_list_name(
        self, list_name: str
    ) -> list[ImmutableDict] | None:
        relationship_collectors = self.get_relationship_collectors()
        if relationship_collectors:
            return [
                block
                for block in relationship_collectors
                if block["for_list"] == list_name
            ]

    def get_unrelated_block_no_answer_values(
        self, unrelated_answer_id: str
    ) -> list[str] | None:
        if unrelated_answers := self.get_answers_by_answer_id(unrelated_answer_id):
            return [
                option["value"]
                for unrelated_answer in unrelated_answers
                for option in unrelated_answer["options"]
                if option.get("action", {}).get("type") == "AddUnrelatedRelationships"
            ]

    @staticmethod
    def get_single_string_value(schema_object: Mapping | str) -> str:
        """
        Resolves an identifying string value for the schema_object. If text_plural the `other` form is returned.
        :return: string value
        """
        if isinstance(schema_object, str):
            return schema_object

        if "text_plural" in schema_object:
            plural_placeholder_string: str = schema_object["text_plural"]["forms"][
                "other"
            ]
            return plural_placeholder_string

        placeholder_string: str = schema_object["text"]
        return placeholder_string

    @staticmethod
    def get_all_questions_for_block(block: Mapping) -> list[ImmutableDict]:
        all_questions: list[ImmutableDict] = []
        if block:
            if block.get("question"):
                all_questions.append(block["question"])
            elif block.get("question_variants"):
                for variant in block["question_variants"]:
                    all_questions.append(variant["question"])

            return all_questions
        return []

    @staticmethod
    def is_primary_person_block_type(block_type: str) -> bool:
        primary_person_blocks = [
            "PrimaryPersonListCollector",
            "PrimaryPersonListAddOrEditQuestion",
        ]

        return block_type in primary_person_blocks

    @staticmethod
    def is_list_block_type(block_type: str) -> bool:
        list_blocks = ["ListCollector"] + LIST_COLLECTOR_CHILDREN
        return block_type in list_blocks

    @staticmethod
    def is_question_block_type(block_type: str) -> bool:
        return block_type in {
            "Question",
            "ListCollectorDrivingQuestion",
            "ConfirmationQuestion",
            "ListRepeatingQuestion",
        }

    @staticmethod
    def has_address_lookup_answer(question: Mapping) -> bool:
        return any(
            answer
            for answer in question["answers"]
            if answer["type"] == "Address" and "lookup_options" in answer
        )

    @staticmethod
    def has_operator(rule: Any) -> bool:
        return isinstance(rule, Mapping) and any(
            operator in rule for operator in OPERATION_MAPPING
        )

    def get_values_for_key(
        self, block: Mapping, key: str, ignore_keys: list[str] | None = None
    ) -> Generator:
        ignore_keys = ignore_keys or []
        for k, v in block.items():
            if k in ignore_keys:
                continue
            if k == key:
                yield v
            if isinstance(v, dict):
                yield from self.get_values_for_key(v, key, ignore_keys)
            elif isinstance(v, (list, tuple)):
                for d in v:
                    # in the case of a when_rule "==": {dict, "Yes"} d could be a string
                    if isinstance(d, dict):
                        yield from self.get_values_for_key(d, key, ignore_keys)

    def _get_parent_section_id_for_block(self, block_id: str) -> str:
        parent_block_id = self._parent_id_map[block_id]
        group_id = self._parent_id_map[parent_block_id]
        section_id = self._parent_id_map[group_id]
        return section_id

    def _block_for_answer(self, answer_id: str) -> ImmutableDict | None:
        question_id = self._parent_id_map[answer_id]
        block_id = self._parent_id_map[question_id]
        parent_block_id = self._parent_id_map[block_id]
        parent_block = self.get_block(parent_block_id)

        if (
            parent_block
            and parent_block["type"] in LIST_COLLECTORS_WITH_REPEATING_BLOCKS
            and block_id not in self.list_collector_repeating_block_ids
        ):
            return parent_block

        return self.get_block(block_id)

    def _group_for_block(self, block_id: str) -> ImmutableDict | None:
        block = self.get_block(block_id)
        parent_id = self._parent_id_map[block_id]
        if block and block["type"] in LIST_COLLECTOR_CHILDREN:
            group_id = self._parent_id_map[parent_id]
            return self.get_group(group_id)

        return self.get_group(parent_id)

    def _get_error_messages(self) -> dict:
        # Force translation of global error messages (stored as LazyString's) into the language of the schema.
        with force_locale(self.language_code):
            messages = {k: str(v) for k, v in error_messages.items()}

        if "messages" in self.json:
            messages.update(self.json["messages"])

        return messages

    def _populate_when_rules_section_dependencies(self) -> None:
        """
        Populates section dependencies for when rules, including when rules containing
        progress value sources.
        Progress section dependencies by section are directly populated in this method.
        Progress section dependencies by block are populated in the
        `self._populate_block_dependencies_for_progress_value_source` called here.
        """
        progress_section_dependencies = (
            self._when_rules_section_dependencies_by_section_for_progress_value_source
        )

        for section in self.get_sections():
            when_rules = self.get_values_for_key(section, "when")
            rules: list = list(when_rules)

            (
                rules_section_dependencies,
                rule_section_dependencies_for_progress_value_source,
                rule_block_dependencies_for_progress_value_source,
            ) = self._get_rules_section_dependencies(section["id"], rules)

            if rules_section_dependencies:
                self._when_rules_section_dependencies_by_section[
                    section["id"]
                ] = rules_section_dependencies

            for (
                key,
                values,
            ) in rule_section_dependencies_for_progress_value_source.items():
                progress_section_dependencies[key].update(values)

            self._populate_block_dependencies_for_progress_value_source(
                rule_block_dependencies_for_progress_value_source
            )

    def _populate_block_dependencies_for_progress_value_source(
        self,
        rule_block_dependencies_for_progress_value_source: dict[
            str, DependencyDictType
        ],
    ) -> None:
        """
        Populates section dependencies for progress value sources at the block level
        """
        dependencies = (
            self._when_rules_block_dependencies_by_section_for_progress_value_source
        )
        for (
            dependent_section,
            section_dependencies_by_block,
        ) in rule_block_dependencies_for_progress_value_source.items():
            for block_id, section_ids in section_dependencies_by_block.items():
                dependencies[dependent_section][block_id].update(section_ids)

    def _get_section_and_block_ids_dependencies_for_progress_source_and_answer_ids_from_rule(
        self, current_section_id: str, rule: Mapping
    ) -> tuple[set[str], dict[str, dict[str, OrderedSet[str] | DependencyDictType]]]:
        """
        For a given rule, returns a set of dependent answer ids and any dependent sections for progress value sources.
        Progress dependencies are keyed both by section and by block e.g.
        sections: {"section-1": {"section-2"}}
        blocks: {"section-1": {"block-1": {"section-2"}}}
        """
        answer_id_list: set[str] = set()
        dependencies_ids_for_progress_value_source: dict[
            str, dict[str, OrderedSet[str] | DependencyDictType]
        ] = {
            "sections": {},
            "blocks": {},
        }
        identifier: str | None = rule.get("identifier")
        source: str | None = rule.get("source")
        selector: str | None = rule.get("selector")

        if source == "answers" and identifier:
            answer_id_list.add(identifier)
        elif source == "calculated_summary" and identifier:
            calculated_summary_block = self.get_block(identifier)
            # Type Ignore: Calculated summary block will exist at this point
            calculated_summary_answer_ids = get_calculated_summary_answer_ids(
                calculated_summary_block  # type: ignore
            )
            answer_id_list.update(calculated_summary_answer_ids)
        elif source == "progress" and identifier:
            if selector == "section" and identifier != current_section_id:
                # Type ignore: Added as this will be a set rather than a dict at this point
                dependencies_ids_for_progress_value_source["sections"][
                    identifier
                ] = OrderedSet(
                    [current_section_id]
                )  # type: ignore
            elif selector == "block" and (
                section_id := self.get_section_id_for_block_id(identifier)
            ):
                # Type ignore: The identifier key will return a list
                if section_id != current_section_id:
                    dependencies_ids_for_progress_value_source["blocks"][section_id] = {
                        identifier: OrderedSet()
                    }
                    dependencies_ids_for_progress_value_source["blocks"][section_id][
                        identifier  # type: ignore
                    ].append(current_section_id)

        return answer_id_list, dependencies_ids_for_progress_value_source

    def _get_rules_section_dependencies(
        self, current_section_id: str, rules: Mapping | Sequence
    ) -> tuple[set[str], DependencyDictType, dict[str, DependencyDictType]]:
        """
        Returns a set of sections ids that the current sections depends on.
        """
        section_dependencies: set[str] = set()
        section_dependencies_for_progress_value_source: dict = {}
        block_dependencies_for_progress_value_source: dict = {}

        if isinstance(rules, Mapping) and QuestionnaireSchema.has_operator(rules):
            rules = self.get_operands(rules)

        for rule in rules:
            if not isinstance(rule, Mapping):
                continue

            [
                answer_id_list,
                dependencies_for_progress_value_source,
            ] = self._get_section_and_block_ids_dependencies_for_progress_source_and_answer_ids_from_rule(
                current_section_id, rule
            )

            section_dependencies_for_progress_value_source.update(
                dependencies_for_progress_value_source["sections"]
            )
            block_dependencies_for_progress_value_source.update(
                dependencies_for_progress_value_source["blocks"]
            )

            # Type Ignore: Added to this method as the block will exist at this point
            for answer_id in answer_id_list:
                block = self.get_block_for_answer_id(answer_id)  # type: ignore
                section_id = self.get_section_id_for_block_id(block["id"])  # type: ignore

                if section_id != current_section_id:
                    self._when_rules_section_dependencies_by_answer[answer_id].add(
                        current_section_id
                    )
                    section_dependencies.add(section_id)  # type: ignore

            if QuestionnaireSchema.has_operator(rule):
                (
                    nested_section_dependencies,
                    nested_section_dependencies_for_progress_value_source,
                    nested_block_dependencies_for_progress_value_source,
                ) = self._get_rules_section_dependencies(current_section_id, rule)
                section_dependencies.update(nested_section_dependencies)
                section_dependencies_for_progress_value_source |= (
                    nested_section_dependencies_for_progress_value_source
                )
                block_dependencies_for_progress_value_source |= (
                    nested_block_dependencies_for_progress_value_source
                )

        return (
            section_dependencies,
            section_dependencies_for_progress_value_source,
            block_dependencies_for_progress_value_source,
        )

    def _populate_calculated_summary_section_dependencies(self) -> None:
        for section in self.get_sections():
            for block in self.get_blocks_for_section(section):
                sources = get_mappings_with_key("source", block, ignore_keys=["when"])

                calculated_summary_sources = [
                    source
                    for source in sources
                    if source["source"] == "calculated_summary"
                ]

                section_dependencies = (
                    self._get_calculated_summary_section_dependencies(
                        sources=calculated_summary_sources,
                    )
                )

                self.calculated_summary_section_dependencies_by_block[section["id"]][
                    block["id"]
                ].update(section_dependencies)

    def _get_calculated_summary_section_dependencies(
        self,
        sources: list[Mapping],
    ) -> set[str]:
        # Type ignore: Added to this method as the block will exist at this point
        section_dependencies: set[str] = set()

        for source in sources:
            answer_id_list: list = []
            identifier: str = source["identifier"]

            calculated_summary_block = self.get_block(identifier)  # type: ignore
            calculated_summary_answer_ids = get_calculated_summary_answer_ids(
                calculated_summary_block  # type: ignore
            )
            answer_id_list.extend(calculated_summary_answer_ids)

            for answer_id in answer_id_list:
                block = self.get_block_for_answer_id(answer_id)  # type: ignore
                section_id = self.get_section_id_for_block_id(block["id"])  # type: ignore

                section_dependencies.add(section_id)  # type: ignore

        return section_dependencies

    def _get_section_ids_for_answer_ids(self, answer_ids: set[str]) -> OrderedSet[str]:
        section_dependencies: OrderedSet[str] = OrderedSet()
        for answer_id in answer_ids:
            block = self.get_block_for_answer_id(answer_id)
            # Type ignore: block_id and section_id is never None
            section_id = self.get_section_id_for_block_id(block["id"])  # type: ignore
            section_dependencies.add(section_id)  # type: ignore
        return section_dependencies

    def get_summary_item_for_list_for_section(
        self, *, section_id: str, list_name: str
    ) -> ImmutableDict | None:
        if summary := self.get_summary_for_section(section_id):
            for item in summary.get("items", []):
                if item.get("for_list") == list_name:
                    return item  # type: ignore

    def get_related_answers_for_list_for_section(
        self, *, section_id: str, list_name: str
    ) -> tuple[ImmutableDict] | None:
        if item := self.get_summary_item_for_list_for_section(
            section_id=section_id, list_name=list_name
        ):
            return item.get("related_answers")

    def get_item_label(self, section_id: str, list_name: str) -> str | None:
        if summary := self.get_summary_for_section(section_id):
            for item in summary.get("items", []):
                if item["for_list"] == list_name and item.get("item_label"):
                    return str(item["item_label"])

    def get_item_anchor(self, section_id: str, list_name: str) -> str | None:
        if summary := self.get_summary_for_section(section_id):
            for item in summary.get("items", []):
                if item["for_list"] == list_name and item.get("item_anchor_answer_id"):
                    return f"#{str(item['item_anchor_answer_id'])}"

    def _populate_placeholder_transform_section_dependencies(self) -> None:
        for block in self.get_blocks():
            transforms = get_mappings_with_key("transform", block)
            placeholder_answer_ids = {
                item["identifier"]
                for transform in transforms
                if transform["transform"] in TRANSFORMS_REQUIRING_ROUTING_PATH
                for item in transform["arguments"]["items"]
                if item.get("source") == "answers"
            }
            placeholder_dependencies = self._get_section_ids_for_answer_ids(
                answer_ids=placeholder_answer_ids
            )
            if placeholder_dependencies:
                # Type Ignore: At this point we section id  and block id cannot be None
                section_id = self.get_section_id_for_block_id(block["id"])
                self._placeholder_transform_section_dependencies_by_block[section_id][  # type: ignore
                    block["id"]
                ].update(
                    placeholder_dependencies
                )

    def update_dependencies_for_dynamic_answers(
        self, *, question: Mapping, block_id: str
    ) -> None:
        if dynamic_answers := question.get("dynamic_answers"):
            self.dynamic_answers_parent_block_ids.add(block_id)
            for answer in dynamic_answers["answers"]:
                value_source = dynamic_answers["values"]
                self._update_answer_dependencies_for_value_source(
                    value_source,
                    block_id=block_id,
                    answer_id=answer["id"],
                )

                self._dynamic_answer_ids.add(answer["id"])

                self._update_answer_dependencies_for_answer(answer, block_id=block_id)


def is_summary_with_calculation(summary_type: str) -> bool:
    return summary_type in {"GrandCalculatedSummary", "CalculatedSummary"}


def get_sources_for_type_from_data(
    *,
    source_type: str,
    data: MultiDict | Mapping | Sequence,
    ignore_keys: list | None = None,
) -> list:
    sources = get_mappings_with_key("source", data, ignore_keys=ignore_keys)

    return [source for source in sources if source["source"] == source_type]


def get_identifiers_from_calculation_block(
    *, calculation_block: Mapping, source_type: str
) -> list[str]:
    values = get_sources_for_type_from_data(
        source_type=source_type, data=calculation_block["calculation"]["operation"]
    )

    return [value["identifier"] for value in values]


def get_calculated_summary_answer_ids(calculated_summary_block: Mapping) -> list[str]:
    if calculated_summary_block["calculation"].get("answers_to_calculate"):
        return list(calculated_summary_block["calculation"]["answers_to_calculate"])

    return get_identifiers_from_calculation_block(
        calculation_block=calculated_summary_block, source_type="answers"
    )


def get_calculation_block_ids_for_grand_calculated_summary(
    grand_calculated_summary_block: Mapping,
) -> list[str]:
    return get_identifiers_from_calculation_block(
        calculation_block=grand_calculated_summary_block,
        source_type="calculated_summary",
    )


def is_list_collector_block_editable(block: Mapping) -> bool:
    return bool(block["type"] == "ListCollector")
