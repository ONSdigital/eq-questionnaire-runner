from collections import abc, defaultdict
from copy import deepcopy
from functools import cached_property
from typing import Any, Generator, Iterable, Mapping, Optional, Sequence, Union

from flask_babel import force_locale
from werkzeug.datastructures import ImmutableDict

from app.data_models.answer import Answer
from app.forms import error_messages
from app.questionnaire.rules.operator import OPERATION_MAPPING

DEFAULT_LANGUAGE_CODE = "en"

LIST_COLLECTOR_CHILDREN = [
    "ListAddQuestion",
    "ListEditQuestion",
    "ListRemoveQuestion",
    "PrimaryPersonListAddOrEditQuestion",
]

RELATIONSHIP_CHILDREN = ["UnrelatedQuestion"]

QuestionSchema = Mapping[str, Any]


class QuestionnaireSchema:  # pylint: disable=too-many-public-methods
    def __init__(
        self, questionnaire_json: Mapping, language_code: str = DEFAULT_LANGUAGE_CODE
    ):
        self._parent_id_map: dict[str, str] = {}
        self._list_name_to_section_map: dict[str, list[str]] = {}
        self._language_code = language_code
        self._questionnaire_json = questionnaire_json
        self._sections_by_id = self._get_sections_by_id()
        self._groups_by_id = self._get_groups_by_id()
        self._blocks_by_id = self._get_blocks_by_id()
        self._questions_by_id = self._get_questions_by_id()
        self._answers_by_id = self._get_answers_by_id()

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
    def survey(self) -> Optional[str]:
        survey: Optional[str] = self.json.get("survey")
        return survey

    @cached_property
    def form_type(self) -> Optional[str]:
        form_type: Optional[str] = self.json.get("form_type")
        return form_type

    @cached_property
    def region_code(self) -> Optional[str]:
        region_code: Optional[str] = self.json.get("region_code")
        return region_code

    @cached_property
    def parent_id_map(self) -> Any:
        return self.serialize(self._parent_id_map)

    @classmethod
    def serialize(cls, data: Any) -> Any:
        if isinstance(data, abc.Hashable):
            return data
        if isinstance(data, list):
            return tuple((cls.serialize(item) for item in data))
        if isinstance(data, dict):
            key_value_tuples = {k: cls.serialize(v) for k, v in data.items()}
            return ImmutableDict(key_value_tuples)

    @classmethod
    def get_mutable_deepcopy(cls, data: Any) -> Any:
        if isinstance(data, tuple):
            return list((cls.get_mutable_deepcopy(item) for item in data))
        if isinstance(data, ImmutableDict):
            key_value_tuples = {k: cls.get_mutable_deepcopy(v) for k, v in data.items()}
            return dict(key_value_tuples)
        return deepcopy(data)

    def _get_sections_by_id(self) -> dict[str, ImmutableDict]:
        return {section["id"]: section for section in self.json.get("sections", [])}

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
                if block["type"] in (
                    "ListCollector",
                    "PrimaryPersonListCollector",
                    "RelationshipCollector",
                ):
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

        for question_set in self._questions_by_id.values():
            for question in question_set:
                question_id = question["id"]
                for answer in question["answers"]:
                    answer_id = answer["id"]
                    self._parent_id_map[answer_id] = question_id

                    answers_by_id[answer["id"]].append(answer)
                    for option in answer.get("options", []):
                        detail_answer = option.get("detail_answer")
                        if detail_answer:
                            detail_answer_id = detail_answer["id"]
                            answers_by_id[detail_answer_id].append(detail_answer)
                            self._parent_id_map[detail_answer_id] = question_id

        return answers_by_id

    @cached_property
    def _flow(self) -> ImmutableDict[str, Any]:
        questionnaire_flow: ImmutableDict = self.json["questionnaire_flow"]
        return questionnaire_flow

    @cached_property
    def flow_options(self) -> ImmutableDict[str, Any]:
        options: ImmutableDict[str, Any] = self._flow["options"]
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

    def get_section_ids_required_for_hub(self) -> list[str]:
        return self.flow_options.get("required_completed_sections", [])

    def get_summary_options(self) -> ImmutableDict[str, Any]:
        return self.flow_options.get("summary", {})

    def get_sections(self) -> Iterable[ImmutableDict]:
        return self._sections_by_id.values()

    def get_section(self, section_id: str) -> Optional[ImmutableDict]:
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
        self, rules: Union[dict, Sequence], list_name: str
    ) -> bool:
        if isinstance(rules, dict) and any(
            operator in rules for operator in OPERATION_MAPPING
        ):
            rules = self.get_operands(rules)

        for rule in rules:
            if not isinstance(rule, dict):
                continue

            # Old rules
            if "list" in rule:
                return rule.get("list") == list_name

            # New rules
            if "source" in rule:
                return (
                    rule.get("source") == "list" and rule.get("identifier") == list_name
                )

            # Nested rules
            if any(operator in rule for operator in OPERATION_MAPPING):
                return self._is_list_name_in_rule(rule, list_name)

    @staticmethod
    def get_operands(rules: dict) -> list:
        operator = next(iter(rules))
        operands: list = rules[operator]
        return operands

    def _section_ids_associated_to_list_name(self, list_name: str) -> list[str]:
        section_ids: list[str] = []

        for section in self.get_sections():
            ignore_keys = ["question_variants", "content_variants"]
            when_rules = self._get_values_for_key(section, "when", ignore_keys)

            rule: Union[dict, list] = next(when_rules, [])
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
    ) -> Optional[ImmutableDict]:
        for block in cls.get_blocks_for_section(section):
            if (
                block["type"] == "ListCollectorDrivingQuestion"
                and list_name == block["for_list"]
            ):
                return block

    def get_remove_block_id_for_list(self, list_name: str) -> Optional[str]:
        for block in self.get_blocks():
            if block["type"] == "ListCollector" and block["for_list"] == list_name:
                remove_block_id: str = block["remove_block"]["id"]
                return remove_block_id

    def get_individual_response_list(self) -> Optional[str]:
        list_name: Optional[str] = self.json.get("individual_response", {}).get(
            "for_list"
        )
        return list_name

    def get_individual_response_show_on_hub(self) -> bool:
        show_on_hub: bool = self.json.get("individual_response", {}).get(
            "show_on_hub", True
        )
        return show_on_hub

    def get_individual_response_individual_section_id(self) -> Optional[str]:
        section_id: Optional[str] = self._questionnaire_json.get(
            "individual_response", {}
        ).get("individual_section_id")
        return section_id

    def get_title_for_section(self, section_id: str) -> Optional[str]:
        if section := self.get_section(section_id):
            return section.get("title")

    def get_show_on_hub_for_section(self, section_id: str) -> Optional[bool]:
        if section := self.get_section(section_id):
            return section.get("show_on_hub", True)

    def get_summary_for_section(self, section_id: str) -> Optional[ImmutableDict]:
        if section := self.get_section(section_id):
            return section.get("summary")

    def get_summary_title_for_section(self, section_id: str) -> Optional[str]:
        if summary := self.get_summary_for_section(section_id):
            return summary.get("title")

    def show_summary_on_completion_for_section(self, section_id: str) -> Optional[bool]:
        if summary := self.get_summary_for_section(section_id):
            return summary.get("show_on_completion", False)

    def get_repeat_for_section(self, section_id: str) -> Optional[ImmutableDict]:
        if section := self.get_section(section_id):
            return section.get("repeat")

    def get_repeating_list_for_section(self, section_id: str) -> Optional[str]:
        if repeat := self.get_repeat_for_section(section_id):
            return repeat.get("for_list")

    def get_repeating_title_for_section(
        self, section_id: str
    ) -> Optional[ImmutableDict]:
        if repeat := self.get_repeat_for_section(section_id):
            return repeat.get("title")

    def get_repeating_page_title_for_section(self, section_id: str) -> Optional[str]:
        if repeat := self.get_repeat_for_section(section_id):
            return repeat.get("page_title")

    def get_custom_page_title_for_section(self, section_id: str) -> Optional[str]:
        if summary := self.get_summary_for_section(section_id):
            return summary.get("page_title")

    def get_section_for_block_id(self, block_id: str) -> Optional[ImmutableDict]:
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

    def get_section_id_for_block_id(self, block_id: str) -> Optional[str]:
        if section := self.get_section_for_block_id(block_id):
            section_id: str = section["id"]
            return section_id

    def get_groups(self) -> Iterable[ImmutableDict]:
        return self._groups_by_id.values()

    def get_group(self, group_id: str) -> Optional[ImmutableDict]:
        return self._groups_by_id.get(group_id)

    def get_group_for_block_id(self, block_id: str) -> Optional[ImmutableDict]:
        return self._group_for_block(block_id)

    def get_first_block_id_for_group(self, group_id: str) -> Optional[str]:
        group = self.get_group(group_id)
        if group:
            block_id: str = group["blocks"][0]["id"]
            return block_id

    def get_first_block_id_for_section(self, section_id: str) -> Optional[str]:
        section = self.get_section(section_id)
        if section:
            group_id: str = section["groups"][0]["id"]
            return self.get_first_block_id_for_group(group_id)

    def get_blocks(self) -> Iterable[ImmutableDict]:
        return self._blocks_by_id.values()

    def get_block(self, block_id: str) -> Optional[ImmutableDict]:
        return self._blocks_by_id.get(block_id)

    def is_block_valid(self, block_id: str) -> bool:
        return bool(self.get_block(block_id))

    def get_block_for_answer_id(self, answer_id: str) -> Optional[ImmutableDict]:
        return self._block_for_answer(answer_id)

    def is_block_in_repeating_section(self, block_id: str) -> Optional[bool]:
        if section_id := self.get_section_id_for_block_id(block_id=block_id):
            return bool(self.get_repeating_list_for_section(section_id))

    def is_answer_in_list_collector_block(self, answer_id: str) -> Optional[bool]:
        if block := self.get_block_for_answer_id(answer_id):
            return self.is_list_block_type(block["type"])

    def is_answer_in_repeating_section(self, answer_id: str) -> Optional[bool]:
        if block := self.get_block_for_answer_id(answer_id):
            return self.is_block_in_repeating_section(block_id=block["id"])

    def is_repeating_answer(
        self,
        answer_id: str,
    ) -> bool:
        return bool(
            self.is_answer_in_list_collector_block(answer_id)
            or self.is_answer_in_repeating_section(answer_id)
        )

    def get_answers_by_answer_id(self, answer_id: str) -> list[ImmutableDict]:
        """Return answers matching answer id, including all matching answers inside
        variants
        """
        answers: list[ImmutableDict] = self._answers_by_id.get(answer_id, [])
        return answers

    def get_default_answer(self, answer_id: str) -> Optional[Answer]:
        if answer_schemas := self.get_answers_by_answer_id(answer_id):
            first_answer_schema = answer_schemas[0]
            try:
                return Answer(first_answer_schema["id"], first_answer_schema["default"])
            except (IndexError, KeyError, TypeError):
                return None
        return None

    def get_add_block_for_list_collector(
        self, list_collector_id: str
    ) -> Optional[ImmutableDict]:
        add_block_map = {
            "ListCollector": "add_block",
            "PrimaryPersonListCollector": "add_or_edit_block",
        }
        if list_collector := self.get_block(list_collector_id):
            add_block: ImmutableDict = list_collector[
                add_block_map[list_collector["type"]]
            ]
            return add_block

    def get_answer_ids_for_list_items(
        self, list_collector_id: str
    ) -> Optional[list[str]]:
        """
        Get answer ids used to add items to a list.
        """
        if add_block := self.get_add_block_for_list_collector(list_collector_id):
            return self.get_answer_ids_for_block(add_block["id"])

    def get_questions(self, question_id: str) -> Optional[list[ImmutableDict]]:
        """Return a list of questions matching some question id
        This includes all questions inside variants
        """
        return self._questions_by_id.get(question_id)

    @staticmethod
    def get_list_collectors_for_list(
        section: Mapping, for_list: str, primary: bool = False
    ) -> Generator[ImmutableDict, None, None]:
        collector_type = "PrimaryPersonListCollector" if primary else "ListCollector"

        return (
            block
            for block in QuestionnaireSchema.get_blocks_for_section(section)
            if block["type"] == collector_type and block["for_list"] == for_list
        )

    @staticmethod
    def get_list_collector_for_list(
        section: Mapping, for_list: str, primary: bool = False
    ) -> Optional[ImmutableDict]:
        try:
            return next(
                QuestionnaireSchema.get_list_collectors_for_list(
                    section, for_list, primary
                )
            )
        except StopIteration:
            return None

    @classmethod
    def get_answer_ids_for_question(cls, question: Mapping) -> list[str]:
        answer_ids: list[str] = []

        for answer in question.get("answers", []):
            answer_ids.append(answer["id"])
            for option in answer.get("options", []):
                if "detail_answer" in option:
                    answer_ids.append(option["detail_answer"]["id"])

        return answer_ids

    def get_first_answer_id_for_block(self, block_id: str) -> str:
        answer_ids = self.get_answer_ids_for_block(block_id)
        return answer_ids[0]

    def get_answer_ids_for_block(self, block_id: str) -> list[str]:
        block = self.get_block(block_id)

        if block:
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
    ) -> Optional[list[ImmutableDict]]:
        relationship_collectors = self.get_relationship_collectors()
        if relationship_collectors:
            return [
                block
                for block in relationship_collectors
                if block["for_list"] == list_name
            ]

    def get_unrelated_block_no_answer_values(
        self, unrelated_answer_id: str
    ) -> Optional[list[str]]:
        if unrelated_answers := self.get_answers_by_answer_id(unrelated_answer_id):
            return [
                option["value"]
                for unrelated_answer in unrelated_answers
                for option in unrelated_answer["options"]
                if option.get("action", {}).get("type") == "AddUnrelatedRelationships"
            ]

    @staticmethod
    def get_single_string_value(schema_object: Union[Mapping, str]) -> str:
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
        return block_type in [
            "Question",
            "ListCollectorDrivingQuestion",
            "ConfirmationQuestion",
        ]

    @staticmethod
    def has_address_lookup_answer(question: Mapping) -> bool:
        return any(
            answer
            for answer in question["answers"]
            if answer["type"] == "Address" and "lookup_options" in answer
        )

    def _get_values_for_key(
        self, block: Mapping, key: str, ignore_keys: list[str] = None
    ) -> Generator:
        ignore_keys = ignore_keys or []
        for k, v in block.items():
            try:
                if k in ignore_keys:
                    continue
                if k == key:
                    yield v
                if isinstance(v, dict):
                    yield from self._get_values_for_key(v, key, ignore_keys)
                elif isinstance(v, (list, tuple)):
                    for d in v:
                        yield from self._get_values_for_key(d, key, ignore_keys)
            except AttributeError:
                continue

    def _get_parent_section_id_for_block(self, block_id: str) -> str:
        parent_block_id = self._parent_id_map[block_id]
        group_id = self._parent_id_map[parent_block_id]
        section_id = self._parent_id_map[group_id]
        return section_id

    def _block_for_answer(self, answer_id: str) -> Optional[ImmutableDict]:
        question_id = self._parent_id_map[answer_id]
        block_id = self._parent_id_map[question_id]
        parent_block_id = self._parent_id_map[block_id]
        parent_block = self.get_block(parent_block_id)

        if parent_block and parent_block["type"] == "ListCollector":
            return parent_block

        return self.get_block(block_id)

    def _group_for_block(self, block_id: str) -> Optional[ImmutableDict]:
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
