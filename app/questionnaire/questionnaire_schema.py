# pylint: disable=too-many-lines
from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass
from decimal import Decimal
from functools import cached_property
from typing import Any, Generator, Iterable, Literal, Mapping, Sequence, TypeAlias

from flask_babel import force_locale
from ordered_set import OrderedSet
from werkzeug.datastructures import ImmutableDict, MultiDict

from app.data_models.answer import Answer
from app.forms import error_messages
from app.questionnaire.rules.operator import OPERATION_MAPPING
from app.questionnaire.schema_utils import get_answers_from_question
from app.settings import MAX_NUMBER
from app.utilities.make_immutable import make_immutable
from app.utilities.mappings import (
    get_flattened_mapping_values,
    get_mappings_with_key,
    get_values_for_key,
)

DEFAULT_LANGUAGE_CODE = "en"

LIST_COLLECTORS_WITH_REPEATING_BLOCKS = {"ListCollector", "ListCollectorContent"}
LIST_COLLECTOR_BLOCKS = {
    "ListCollector",
    "ListCollectorContent",
    "PrimaryPersonListCollector",
    "RelationshipCollector",
}

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
TRANSFORMS_REQUIRING_UNRESOLVED_ARGUMENTS = ["format_currency"]

NUMERIC_ANSWER_TYPES = {
    "Currency",
    "Duration",
    "Number",
    "Percentage",
    "Unit",
}


class InvalidSchemaConfigurationException(Exception):
    pass


@dataclass(frozen=True)
class Dependent:
    """Represents a dependent belonging to some answer or list.

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
        self._list_collector_section_ids_by_list_name: dict[str, list[str]] = (
            defaultdict(list)
        )
        self._answer_dependencies_map: dict[str, set[Dependent]] = defaultdict(set)
        self._list_dependencies_map: dict[str, set[Dependent]] = defaultdict(set)
        self._when_rules_section_dependencies_by_section: dict[str, set[str]] = (
            defaultdict(set)
        )
        self._when_rules_section_dependencies_by_section_for_progress_value_source: (
            defaultdict[str, OrderedSet[str]]
        ) = defaultdict(
            OrderedSet
        )
        self._when_rules_block_dependencies_by_section_for_progress_value_source: (
            defaultdict[str, DependencyDictType]
        ) = defaultdict(
            lambda: defaultdict(OrderedSet)
        )
        self.calculation_summary_section_dependencies_by_block: dict[
            str, DependencyDictType
        ] = defaultdict(lambda: defaultdict(OrderedSet))
        self._when_rules_section_dependencies_by_answer: dict[str, set[str]] = (
            defaultdict(set)
        )
        self._when_rules_section_dependencies_by_list: dict[str, set[str]] = (
            defaultdict(set)
        )
        self._placeholder_transform_section_dependencies_by_block: dict[
            str, dict[str, set[str]]
        ] = defaultdict(lambda: defaultdict(set))
        self._language_code = language_code
        self._questionnaire_json = questionnaire_json
        self._min_and_max_map: dict[str, dict[str, int]] = defaultdict(
            lambda: defaultdict(int)
        )
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

        # Post schema parsing.
        self._populate_answer_and_list_dependencies()
        self._populate_when_rules_section_dependencies()
        self._populate_calculation_summary_section_dependencies()
        self._populate_min_max_for_numeric_answers()
        self._populate_placeholder_transform_section_dependencies()

    @property
    def placeholder_transform_section_dependencies_by_block(
        self,
    ) -> dict[str, dict[str, set[str]]]:
        return self._placeholder_transform_section_dependencies_by_block

    @cached_property
    def answer_dependencies(self) -> ImmutableDict[str, set[Dependent]]:
        return ImmutableDict(self._answer_dependencies_map)

    @cached_property
    def list_dependencies(self) -> ImmutableDict[str, set[Dependent]]:
        return ImmutableDict(self._list_dependencies_map)

    @cached_property
    # Type ignore: make_immutable uses generic types so return type is manually specified
    def min_and_max_map(self) -> ImmutableDict[str, ImmutableDict[str, int]]:
        return make_immutable(self._min_and_max_map)  # type: ignore

    def _create_min_max_map(
        self,
        min_max: Literal["minimum", "maximum"],
        answer_id: str,
        answers: Iterable[ImmutableDict],
        default_min_max: int,
    ) -> None:
        longest_value_length = 0
        for answer in answers:
            value = answer.get(min_max, {}).get("value")

            if isinstance(value, float | int | Decimal):
                # Factor out the decimals as it's accounted for in jinja_filters.py
                value_length = len(str(int(value)))

                longest_value_length = max(longest_value_length, value_length)

            elif isinstance(value, Mapping) and value:
                if value.get("source") == "answers":
                    longest_value_length = max(
                        longest_value_length,
                        self._min_and_max_map[value["identifier"]][min_max],
                    )

        self._min_and_max_map[answer_id][min_max] = (
            longest_value_length or default_min_max
        )

    def _populate_min_max_for_numeric_answers(self) -> None:
        for answer_id, answers in self._answers_by_id.items():
            # validator ensures all answers will be of the same type so its sufficient to only check the first
            if answers[0]["type"] in NUMERIC_ANSWER_TYPES:
                self._create_min_max_map("minimum", answer_id, answers, 1)
                self._create_min_max_map(
                    "maximum", answer_id, answers, len(str(MAX_NUMBER))
                )

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

    @cached_property
    def supplementary_lists(self) -> frozenset[str]:
        return frozenset(self.json.get("supplementary_data", {}).get("lists", []))

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

    @cached_property
    def list_collector_section_ids_by_list_name(self) -> ImmutableDict[str, tuple[str]]:
        # Type ignore: make_immutable is generic so type is manually specified
        return make_immutable(self._list_collector_section_ids_by_list_name)  # type: ignore

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

    def get_when_rule_section_dependencies_for_list(self, list_name: str) -> set[str]:
        """Gets the set of all sections which reference the list in a when rule somewhere"""
        return self._when_rules_section_dependencies_by_list.get(list_name, set())

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
                if block["type"] in LIST_COLLECTOR_BLOCKS:
                    self._list_collector_section_ids_by_list_name[
                        block["for_list"]
                    ].append(self._parent_id_map[group["id"]])
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

    def _populate_answer_and_list_dependencies(self) -> None:
        for block in self.get_blocks():
            if block["type"] in {"CalculatedSummary", "GrandCalculatedSummary"}:
                self._update_dependencies_for_summary(block)
                continue

            if block["type"] == "ListCollectorContent" and block.get(
                "repeating_blocks"
            ):
                # Editable list collectors don't need this because the add/remove handlers manage revisiting repeating blocks
                self._list_dependencies_map[block["for_list"]].add(
                    self._get_dependent_for_block_id(block_id=block["id"])
                )

            for question in self.get_all_questions_for_block(block):
                self.update_dependencies_for_dynamic_answers(
                    question=question, block_id=block["id"]
                )

                if question["type"] == "Calculated":
                    self._update_dependencies_for_calculations(
                        question["calculations"], block_id=block["id"]
                    )
                    continue

                for answer in question.get("answers", []):
                    self._update_dependencies_for_answer(answer, block_id=block["id"])
                    for option in answer.get("options", []):
                        if "detail_answer" in option:
                            self._update_dependencies_for_answer(
                                option["detail_answer"], block_id=block["id"]
                            )

    def _update_dependencies_for_summary(self, block: ImmutableDict) -> None:
        if block["type"] == "CalculatedSummary":
            self._update_dependencies_for_calculated_summary_dependency(
                calculated_summary_block=block, dependent_block=block
            )
        elif block["type"] == "GrandCalculatedSummary":
            self._update_dependencies_for_grand_calculated_summary(block)

    def _update_dependencies_for_calculated_summary_dependency(
        self, *, calculated_summary_block: ImmutableDict, dependent_block: ImmutableDict
    ) -> None:
        """
        For a block that depends on a calculated summary block, add the block as a dependency of each of the calculated summary answers
        Similarly if the calculated summary depends on a list, then add the block as a dependency of the list
        """
        calculated_summary_answer_ids = get_calculated_summary_answer_ids(
            calculated_summary_block
        )
        dependent = self._get_dependent_for_block_id(block_id=dependent_block["id"])
        for answer_id in calculated_summary_answer_ids:
            if list_name := self.get_list_name_for_answer_id(answer_id):
                # dynamic/repeating answers means the calculated summary also depends on the list those answers loop over
                self._list_dependencies_map[list_name].add(dependent)
            self._answer_dependencies_map[answer_id].add(dependent)

    def _update_dependencies_for_grand_calculated_summary(
        self, grand_calculated_summary_block: ImmutableDict
    ) -> None:
        grand_calculated_summary_calculated_summary_ids = (
            get_calculated_summary_ids_for_grand_calculated_summary(
                grand_calculated_summary_block
            )
        )
        for calculated_summary_id in grand_calculated_summary_calculated_summary_ids:
            # Type ignore: safe to assume block exists
            calculated_summary_block: ImmutableDict = self.get_block(calculated_summary_id)  # type: ignore
            self._update_dependencies_for_calculated_summary_dependency(
                calculated_summary_block=calculated_summary_block,
                dependent_block=grand_calculated_summary_block,
            )

    def _update_dependencies_for_calculations(
        self, calculations: tuple[ImmutableDict, ...], *, block_id: str
    ) -> None:
        for calculation in calculations:
            if source_answer_id := calculation.get("answer_id"):
                dependents = {
                    self._get_dependent_for_block_id(
                        block_id=self.get_block_for_answer_id(answer_id)["id"]  # type: ignore
                    )
                    for answer_id in calculation["answers_to_calculate"]
                }
                self._answer_dependencies_map[source_answer_id] |= dependents

            elif isinstance(calculation.get("value"), dict):
                self._update_dependencies_for_value_source(
                    calculation["value"],
                    block_id=block_id,
                )

    def _update_dependencies_for_answer(
        self, answer: Mapping, *, block_id: str
    ) -> None:
        for key in ["minimum", "maximum"]:
            value = answer.get(key, {}).get("value")
            if isinstance(value, dict):
                self._update_dependencies_for_value_source(
                    value,
                    block_id=block_id,
                )

        if dynamic_options_values := answer.get("dynamic_options", {}).get("values"):
            self._update_dependencies_for_dynamic_options(
                dynamic_options_values, block_id=block_id, answer_id=answer["id"]
            )

    def _update_dependencies_for_dynamic_options(
        self,
        dynamic_options_values: Mapping,
        *,
        block_id: str,
        answer_id: str,
    ) -> None:
        value_sources = get_mappings_with_key("source", data=dynamic_options_values)
        for value_source in value_sources:
            self._update_dependencies_for_value_source(
                value_source, block_id=block_id, answer_id=answer_id
            )

    def _update_dependencies_for_calculated_summary_value_source(
        self, *, calculated_summary_id: str, block_id: str, answer_id: str | None
    ) -> None:
        """
        For the given block (and optionally answer within) set it as a dependency of each calculated summary answer
        If the calculated summary depends on a list, make the block depend on it too
        """
        # Type ignore: validator checks the validity of value sources.
        calculated_summary_block: ImmutableDict = self.get_block(calculated_summary_id)  # type: ignore
        answer_ids_for_block = get_calculated_summary_answer_ids(
            calculated_summary_block
        )
        dependent = self._get_dependent_for_block_id(
            block_id=block_id, answer_id=answer_id
        )
        for answer_id_for_block in answer_ids_for_block:
            self._answer_dependencies_map[answer_id_for_block].add(dependent)
            # if the answer is repeating, then the calculated summary also depends on the list it loops over
            if list_name := self.get_list_name_for_answer_id(answer_id_for_block):
                self._list_dependencies_map[list_name].add(dependent)

    def _update_dependencies_for_value_source(
        self,
        value_source: Mapping,
        *,
        block_id: str,
        answer_id: str | None = None,
    ) -> None:
        """
        For a given value source, get the answer ids it consists of, or the list it references,
        and add the given block (and optionally answer) as a dependency of those answers or lists
        """
        if value_source["source"] == "answers":
            self._answer_dependencies_map[value_source["identifier"]] |= {
                self._get_dependent_for_block_id(block_id=block_id, answer_id=answer_id)
            }
        elif value_source["source"] == "calculated_summary":
            identifier = value_source["identifier"]
            self._update_dependencies_for_calculated_summary_value_source(
                calculated_summary_id=identifier, block_id=block_id, answer_id=answer_id
            )

        elif value_source["source"] == "grand_calculated_summary":
            identifier = value_source["identifier"]
            # Type ignore: validator will ensure identifier is valid
            grand_calculated_summary_block: ImmutableDict = self.get_block(identifier)  # type: ignore
            for (
                calculated_summary_id
            ) in get_calculated_summary_ids_for_grand_calculated_summary(
                grand_calculated_summary_block
            ):
                self._update_dependencies_for_calculated_summary_value_source(
                    calculated_summary_id=calculated_summary_id,
                    block_id=block_id,
                    answer_id=answer_id,
                )

        if value_source["source"] == "list":
            self._list_dependencies_map[value_source["identifier"]].add(
                self._get_dependent_for_block_id(block_id=block_id)
            )

    def _get_dependent_for_block_id(
        self,
        *,
        block_id: str,
        answer_id: str | None = None,
        for_list: str | None = None,
    ) -> Dependent:
        section_id: str = self.get_section_id_for_block_id(block_id)  # type: ignore
        if not for_list:
            for_list = self.get_repeating_list_for_section(section_id)

        return Dependent(
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
        # Type ignore: the type of the .get() returned value is Any
        return self.flow_options.get("required_completed_sections", tuple())  # type: ignore

    def get_summary_options(self) -> ImmutableDict[str, bool]:
        # Type ignore: the type of the .get() returned value is Any
        return self.flow_options.get("summary", ImmutableDict({}))  # type: ignore

    def get_sections(self) -> Iterable[ImmutableDict]:
        return self._sections_by_id.values()

    def get_section_ids(self) -> Iterable[str]:
        return self._sections_by_id.keys()

    def get_section(self, section_id: str) -> ImmutableDict | None:
        return self._sections_by_id.get(section_id)

    def get_submission(self) -> ImmutableDict:
        schema: ImmutableDict = self.json.get("submission", ImmutableDict({}))
        return schema

    def get_post_submission(self) -> ImmutableDict:
        schema: ImmutableDict = self.json.get("post_submission", ImmutableDict({}))
        return schema

    @staticmethod
    def get_operands(rules: Mapping) -> Sequence:
        operator = next(iter(rules))
        operands: Sequence = rules[operator]
        return operands

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
        # Type ignore: the type of the .get() returned value is Any
        if section := self.get_section(section_id):
            return section.get("show_on_hub", True)  # type: ignore

    def get_summary_for_section(self, section_id: str) -> ImmutableDict | None:
        if section := self.get_section(section_id):
            return section.get("summary")

    def get_summary_title_for_section(self, section_id: str) -> str | None:
        if summary := self.get_summary_for_section(section_id):
            return summary.get("title")

    def show_summary_on_completion_for_section(self, section_id: str) -> bool | None:
        if summary := self.get_summary_for_section(section_id):
            # Type ignore: the type of the .get() returned value is Any
            return summary.get("show_on_completion", False)  # type: ignore

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

    def get_list_name_for_answer_id(self, answer_id: str) -> str | None:
        """
        if the answer is dynamic or in a repeating block or section, return the name of the list it repeats over, otherwise None.
        """
        # Type ignore: safe to assume block exists, same for section below.
        block: ImmutableDict = self.get_block_for_answer_id(answer_id)  # type: ignore
        block_id: str = block["id"]
        if self.is_answer_dynamic(answer_id):
            return self.get_list_name_for_dynamic_answer(block_id)
        if self.is_answer_in_list_collector_repeating_block(answer_id):
            return self.list_names_by_list_repeating_block_id[block_id]
        if self.is_answer_in_list_collector_block(answer_id):
            return block["for_list"]  # type: ignore
        if self.is_answer_in_repeating_section(answer_id):
            section_id: str = self.get_section_id_for_block_id(block_id)  # type: ignore
            return self.get_repeating_list_for_section(section_id)

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
            add_block: ImmutableDict | None = list_collector.get(
                add_block_map.get(list_collector["type"])
            )
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
            # Type ignore: the type of the .get() returned value is Any
            return list_collector.get("repeating_blocks", [])  # type: ignore

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

    def get_list_collectors_for_list_for_sections(
        self, sections: list[str], for_list: str, primary: bool = False
    ) -> list[ImmutableDict]:
        blocks: list[ImmutableDict] = []
        for section_id in sections:
            if section := self.get_section(section_id):
                collector_type = (
                    {"PrimaryPersonListCollector"}
                    if primary
                    else LIST_COLLECTORS_WITH_REPEATING_BLOCKS
                )

                blocks.extend(
                    block
                    for block in self.get_blocks_for_section(section)
                    if block["type"] in collector_type and block["for_list"] == for_list
                )

        return blocks

    def get_list_collectors_for_list(
        self, for_list: str, primary: bool = False, section_id: str | None = None
    ) -> list[ImmutableDict]:
        sections = (
            [section_id]
            if section_id
            else self._list_collector_section_ids_by_list_name[for_list]
        )

        return self.get_list_collectors_for_list_for_sections(
            sections, for_list, primary
        )

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
        answer_ids = get_calculated_summary_answer_ids(calculated_summary_block)
        decimal_limit = self.get_decimal_limit(answer_ids)
        first_answer_id = answer_ids[0]
        first_answer = self.get_answers_by_answer_id(first_answer_id)[0]
        return {
            "type": first_answer["type"].lower(),
            "unit": first_answer.get("unit"),
            "unit_length": first_answer.get("unit_length"),
            "currency": first_answer.get("currency"),
            "decimal_places": decimal_limit,
        }

    def get_decimal_limit_from_calculated_summaries(
        self, calculated_summary_block_ids: list[str]
    ) -> int | None:
        """
        Get the max number of decimal places from the calculated summary block(s) passed in
        """
        decimal_limits: list[int] = []
        for calculated_summary_id in calculated_summary_block_ids:
            # Type ignore: the block will exist for any valid calculated summary id
            answer_ids = get_calculated_summary_answer_ids(self.get_block(calculated_summary_id))  # type: ignore
            if (decimal_limit := self.get_decimal_limit(answer_ids)) is not None:
                decimal_limits.append(decimal_limit)
        return max(decimal_limits, default=None)

    def get_decimal_limit(self, answer_ids: list[str]) -> int | None:
        decimal_limits: list[int] = [
            decimal_places
            for answer_id in answer_ids
            for answer in self.get_answers_by_answer_id(answer_id)
            if (decimal_places := answer.get("decimal_places")) is not None
        ]
        return max(decimal_limits, default=None)

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
        Populates section dependencies for when rules, including when rules containing progress value sources.

        Question variants and content variants don't need including, since the answer ids, block ids, and question ids
        remain the same, so a change in the variant, does not impact questionnaire progress.
        """
        for section in self.get_sections():
            rules: list[Mapping] = []
            when_rules = get_values_for_key(
                "when",
                data=section,
                ignore_keys=["question_variants", "content_variants"],
            )
            for when_rule in when_rules:
                rules.extend(get_mappings_with_key("source", data=when_rule))

            for rule in rules:
                self._populate_dependencies_for_rule(
                    rule, current_section_id=section["id"]
                )

    def _populate_dependencies_for_rule(
        self, rule: Mapping, *, current_section_id: str
    ) -> None:
        """
        For a given rule, update dependency maps to indicate that the section containing the rule
        depends on the answer/block/progress etc. that the rule is referencing.
        """
        identifier: str = rule["identifier"]
        source: str = rule["source"]
        selector: str | None = rule.get("selector")

        dependent_answer_ids: set[str] = set()
        dependent_section_ids: set[str] = set()

        progress_section_dependencies = (
            self._when_rules_section_dependencies_by_section_for_progress_value_source
        )
        progress_block_dependencies = (
            self._when_rules_block_dependencies_by_section_for_progress_value_source
        )

        if source == "answers":
            dependent_answer_ids.add(identifier)
        elif source == "calculated_summary":
            calculated_summary_block = self.get_block(identifier)
            # Type Ignore: Calculated summary block will exist at this point
            calculated_summary_answer_ids = get_calculated_summary_answer_ids(
                calculated_summary_block  # type: ignore
            )
            dependent_answer_ids.update(calculated_summary_answer_ids)
        elif source == "grand_calculated_summary":
            # grand calculated summary section could differ from cs & answer sections, include it in dependent sections
            grand_calculated_summary_section_id: str = self.get_section_id_for_block_id(identifier)  # type: ignore
            if grand_calculated_summary_section_id != current_section_id:
                dependent_section_ids.add(grand_calculated_summary_section_id)
            dependent_answer_ids.update(
                self.get_answer_ids_for_grand_calculated_summary_id(identifier)
            )
        elif source == "list":
            self._when_rules_section_dependencies_by_list[identifier].add(
                current_section_id
            )
        elif source == "progress":
            if selector == "section" and identifier != current_section_id:
                progress_section_dependencies[identifier].add(current_section_id)
            elif (
                selector == "block"
                and (block_section_id := self.get_section_id_for_block_id(identifier))
                != current_section_id
            ):
                # Type ignore: The identifier key will return a list
                progress_block_dependencies[block_section_id][identifier].add(  # type: ignore
                    current_section_id
                )

        dependent_section_ids |= self._get_section_dependencies_for_dependent_answers(
            current_section_id, dependent_answer_ids
        )
        if dependent_section_ids:
            self._when_rules_section_dependencies_by_section[current_section_id].update(
                dependent_section_ids
            )

    def _get_section_dependencies_for_dependent_answers(
        self, current_section_id: str, dependent_answer_ids: Iterable[str]
    ) -> set[str]:
        """
        For a set of answer ids dependent on a rule in the current section, add the current section
        as a dependency of the answer and return the set of sections those answers reside in.
        """
        section_dependencies: set[str] = set()
        # Type Ignore: Added to this method as the block will exist at this point
        for answer_id in dependent_answer_ids:
            block = self.get_block_for_answer_id(answer_id)
            section_id = self.get_section_id_for_block_id(block["id"])  # type: ignore
            if section_id != current_section_id:
                self._when_rules_section_dependencies_by_answer[answer_id].add(
                    current_section_id
                )
                section_dependencies.add(section_id)  # type: ignore
        return section_dependencies

    def _populate_calculation_summary_section_dependencies(self) -> None:
        """
        For each block, find all the calculated and grand calculated summary value source dependencies
        and make sure all involved sections are added as dependencies for that block and its section.

        Since calculated summaries can only contain answers from the section they are in,
        it is sufficient to check the section for the calculated summary only. For grand calculated summaries
        Need to include the section of the gcs, and each cs it references.
        """
        for section in self.get_sections():
            for block in self.get_blocks_for_section(section):
                sources = get_mappings_with_key(
                    "source", data=block, ignore_keys=["when"]
                )
                section_dependencies: set[str] = set()

                for source in sources:
                    if source["source"] == "calculated_summary":
                        section_dependencies.add(
                            self.get_section_id_for_block_id(source["identifier"])  # type: ignore
                        )
                    elif source["source"] == "grand_calculated_summary":
                        section_dependencies.update(
                            self.get_section_ids_for_grand_calculated_summary_id(
                                source["identifier"]
                            )
                        )
                self.calculation_summary_section_dependencies_by_block[section["id"]][
                    block["id"]
                ].update(section_dependencies)

    def _get_section_ids_for_answer_ids(
        self, answer_ids: Iterable[str]
    ) -> OrderedSet[str]:
        section_dependencies: OrderedSet[str] = OrderedSet()
        for answer_id in answer_ids:
            block = self.get_block_for_answer_id(answer_id)
            # Type ignore: block_id and section_id is never None
            section_id = self.get_section_id_for_block_id(block["id"])  # type: ignore
            section_dependencies.add(section_id)  # type: ignore
        return section_dependencies

    def get_answer_ids_for_grand_calculated_summary_id(
        self, grand_calculated_summary_id: str
    ) -> list[str]:
        # Type ignores: can assume the cs and gcs exist
        answer_ids: list[str] = []
        block: ImmutableDict = self.get_block(grand_calculated_summary_id)  # type: ignore
        for (
            calculated_summary_id
        ) in get_calculated_summary_ids_for_grand_calculated_summary(block):
            calculated_summary_block: ImmutableDict = self.get_block(  # type: ignore
                calculated_summary_id
            )
            answer_ids.extend(
                get_calculated_summary_answer_ids(calculated_summary_block)
            )
        return answer_ids

    def get_section_ids_for_grand_calculated_summary_id(
        self, grand_calculated_summary_id: str
    ) -> set[str]:
        """
        Returns all sections that the grand calculated summary depends on,
        i.e. the grand calculated summary section and the sections for each included calculated summary
        """
        # Type ignores: Can assume the block and each section exists
        block_ids = {grand_calculated_summary_id}
        block: ImmutableDict = self.get_block(grand_calculated_summary_id)  # type: ignore
        block_ids.update(get_calculated_summary_ids_for_grand_calculated_summary(block))
        return {self.get_section_id_for_block_id(block_id) for block_id in block_ids}  # type: ignore

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

    def _update_dependencies_for_placeholders(
        self, answer_ids: Iterable[str], block: ImmutableDict
    ) -> None:
        if dependent_sections := self._get_section_ids_for_answer_ids(
            answer_ids=answer_ids
        ):
            # Type Ignore: At this point the section id and block id cannot be None
            section_id = self.get_section_id_for_block_id(block["id"])
            self._placeholder_transform_section_dependencies_by_block[section_id][  # type: ignore
                block["id"]
            ].update(
                dependent_sections
            )

    def _populate_placeholder_transform_section_dependencies(self) -> None:
        for block in self.get_blocks():
            # Calculation summary blocks can indirectly reference placeholders from their dependent blocks, so
            # logic is needed to identify the relevant dependent blocks that may contain placeholders and assess
            # whether there are any dependent sections
            if block["type"] == "GrandCalculatedSummary":
                answer_ids = self.get_answer_ids_for_grand_calculated_summary_id(
                    block["id"]
                )
            elif block["type"] == "CalculatedSummary":
                answer_ids = get_calculated_summary_answer_ids(block)
            else:
                answer_ids = []

            if answer_ids:
                dependent_blocks = [
                    self.get_block_for_answer_id(answer_id)
                    for answer_id in set(answer_ids)
                ]
                for dependent_block in dependent_blocks:
                    # Type ignore: Block will exist at this point
                    if placeholder_answer_ids := get_placeholder_answer_ids_requiring_routing_path(
                        dependent_block  # type: ignore
                    ):
                        self._update_dependencies_for_placeholders(
                            placeholder_answer_ids, block
                        )

            elif placeholder_answer_ids := get_placeholder_answer_ids_requiring_routing_path(
                block
            ):
                self._update_dependencies_for_placeholders(
                    placeholder_answer_ids, block
                )

    def update_dependencies_for_dynamic_answers(
        self, *, question: Mapping, block_id: str
    ) -> None:
        if dynamic_answers := question.get("dynamic_answers"):
            self.dynamic_answers_parent_block_ids.add(block_id)
            for answer in dynamic_answers["answers"]:
                value_source = dynamic_answers["values"]
                self._update_dependencies_for_value_source(
                    value_source,
                    block_id=block_id,
                    answer_id=answer["id"],
                )

                self._dynamic_answer_ids.add(answer["id"])

                self._update_dependencies_for_answer(answer, block_id=block_id)


def is_summary_with_calculation(summary_type: str) -> bool:
    return summary_type in {"GrandCalculatedSummary", "CalculatedSummary"}


def get_sources_for_types_from_data(
    *,
    source_types: Iterable[str],
    data: MultiDict | Mapping | Sequence,
    ignore_keys: list | None = None,
) -> list:
    sources = get_mappings_with_key(key="source", data=data, ignore_keys=ignore_keys)

    return [source for source in sources if source["source"] in source_types]


def get_identifiers_from_calculation_block(
    *, calculation_block: Mapping, source_type: str
) -> list[str]:
    values = get_sources_for_types_from_data(
        source_types={source_type}, data=calculation_block["calculation"]["operation"]
    )

    return [value["identifier"] for value in values]


def get_calculated_summary_answer_ids(calculated_summary_block: Mapping) -> list[str]:
    if calculated_summary_block["calculation"].get("answers_to_calculate"):
        return list(calculated_summary_block["calculation"]["answers_to_calculate"])

    return get_identifiers_from_calculation_block(
        calculation_block=calculated_summary_block, source_type="answers"
    )


def get_calculated_summary_ids_for_grand_calculated_summary(
    grand_calculated_summary_block: Mapping,
) -> list[str]:
    return get_identifiers_from_calculation_block(
        calculation_block=grand_calculated_summary_block,
        source_type="calculated_summary",
    )


def is_list_collector_block_editable(block: Mapping) -> bool:
    return bool(block["type"] == "ListCollector")


def get_placeholder_answer_ids_requiring_routing_path(block: ImmutableDict) -> set[str]:
    transforms = get_mappings_with_key("transform", data=block)

    return {
        item["identifier"]
        for transform in transforms
        if transform["transform"] in TRANSFORMS_REQUIRING_ROUTING_PATH
        for item in transform["arguments"]["items"]
        if item.get("source") == "answers"
    }
