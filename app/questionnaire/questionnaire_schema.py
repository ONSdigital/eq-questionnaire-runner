from collections import abc, defaultdict
from copy import deepcopy
from functools import cached_property
from typing import List, Mapping, Union

from flask_babel import force_locale
from werkzeug.datastructures import ImmutableDict

from app.data_models.answer import Answer
from app.forms import error_messages
from app.questionnaire.schema_utils import get_values_for_key

DEFAULT_LANGUAGE_CODE = "en"

LIST_COLLECTOR_CHILDREN = [
    "ListAddQuestion",
    "ListEditQuestion",
    "ListRemoveQuestion",
    "PrimaryPersonListAddOrEditQuestion",
]

RELATIONSHIP_CHILDREN = ["UnrelatedQuestion"]


class QuestionnaireSchema:  # pylint: disable=too-many-public-methods
    def __init__(self, questionnaire_json, language_code=DEFAULT_LANGUAGE_CODE):
        self._parent_id_map = {}
        self._list_name_to_section_map = {}
        self._language_code = language_code
        self._questionnaire_json = questionnaire_json
        self._sections_by_id = self._get_sections_by_id()
        self._groups_by_id = self._get_groups_by_id()
        self._blocks_by_id = self._get_blocks_by_id()
        self._questions_by_id = self._get_questions_by_id()
        self._answers_by_id = self._get_answers_by_id()

    @cached_property
    def language_code(self):
        return self._language_code

    @cached_property
    def error_messages(self):
        return self.serialize(self._get_error_messages())

    @cached_property
    def json(self):
        return self.serialize(self._questionnaire_json)

    @cached_property
    def survey(self):
        return self.json.get("survey")

    @cached_property
    def form_type(self):
        return self.json.get("form_type")

    @cached_property
    def region_code(self):
        return self.json.get("region_code")

    @cached_property
    def parent_id_map(self):
        return self.serialize(self._parent_id_map)

    @classmethod
    def serialize(cls, data):
        if isinstance(data, abc.Hashable):
            return data
        if isinstance(data, list):
            return tuple((cls.serialize(item) for item in data))
        if isinstance(data, dict):
            key_value_tuples = {k: cls.serialize(v) for k, v in data.items()}
            return ImmutableDict(key_value_tuples)

    @classmethod
    def get_mutable_deepcopy(cls, data):
        if isinstance(data, tuple):
            return list((cls.get_mutable_deepcopy(item) for item in data))
        if isinstance(data, ImmutableDict):
            key_value_tuples = {k: cls.get_mutable_deepcopy(v) for k, v in data.items()}
            return dict(key_value_tuples)
        return deepcopy(data)

    def _get_sections_by_id(self):
        return {section["id"]: section for section in self.json.get("sections", [])}

    def _get_groups_by_id(self):
        groups_by_id = {}

        for section in self._sections_by_id.values():
            for group in section["groups"]:
                group_id = group["id"]
                groups_by_id[group_id] = group
                self._parent_id_map[group_id] = section["id"]

        return groups_by_id

    def _get_blocks_by_id(self):
        blocks = {}

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

    def _get_questions_by_id(self):
        questions_by_id = defaultdict(list)

        for block in self._blocks_by_id.values():
            questions = self.get_all_questions_for_block(block)
            for question in questions:
                question_id = question["id"]
                questions_by_id[question_id].append(question)
                self._parent_id_map[question_id] = block["id"]

        return questions_by_id

    def _get_answers_by_id(self):
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

    def get_hub(self):
        return self.json.get("hub", {})

    def is_hub_enabled(self):
        return self.get_hub().get("enabled")

    def get_section_ids_required_for_hub(self):
        return self.get_hub().get("required_completed_sections", [])

    def get_sections(self):
        return self._sections_by_id.values()

    def get_section_ids(self):
        return list(self._sections_by_id.keys())

    def get_section(self, section_id: str):
        return self._sections_by_id.get(section_id)

    def get_section_ids_dependent_on_list(self, list_name: str) -> List:
        try:
            return self._list_name_to_section_map[list_name]
        except KeyError:
            section_ids = self._section_ids_associated_to_list_name(list_name)
            self._list_name_to_section_map[list_name] = section_ids
            return section_ids

    def get_submission(self):
        return self.json.get("submission", {})

    def _section_ids_associated_to_list_name(self, list_name: str) -> List:
        section_ids: List = []

        for section in self.get_sections():
            ignore_keys = {"question_variants", "content_variants"}
            when_rules = get_values_for_key(section, "when", ignore_keys)

            if any(
                rule.get("list") == list_name
                for when_rule in when_rules
                for rule in when_rule
            ):
                section_ids.append(section["id"])

        return section_ids

    @staticmethod
    def get_blocks_for_section(section):
        return (block for group in section["groups"] for block in group["blocks"])

    @classmethod
    def get_driving_question_for_list(cls, section, list_name):
        for block in cls.get_blocks_for_section(section):
            if (
                block["type"] == "ListCollectorDrivingQuestion"
                and list_name == block["for_list"]
            ):
                return block

    def get_remove_block_id_for_list(self, list_name):
        for block in self.get_blocks():
            if block["type"] == "ListCollector" and block["for_list"] == list_name:
                return block["remove_block"]["id"]

    def get_individual_response_list(self):
        return self.json.get("individual_response", {}).get("for_list")

    def get_individual_response_show_on_hub(self):
        return self.json.get("individual_response", {}).get("show_on_hub", True)

    def get_individual_response_individual_section_id(self):
        return self._questionnaire_json.get("individual_response", {}).get(
            "individual_section_id"
        )

    def get_title_for_section(self, section_id):
        return self._sections_by_id.get(section_id).get("title")

    def get_show_on_hub_for_section(self, section_id):
        return self._sections_by_id.get(section_id).get("show_on_hub", True)

    def get_summary_for_section(self, section_id: str) -> Mapping:
        return self._sections_by_id.get(section_id).get("summary", {})

    def get_summary_title_for_section(self, section_id: str):
        return self.get_summary_for_section(section_id).get("title")

    def show_summary_on_completion_for_section(self, section_id: str) -> bool:
        return self.get_summary_for_section(section_id).get("show_on_completion", False)

    def get_repeat_for_section(self, section_id):
        return self._sections_by_id.get(section_id).get("repeat", {})

    def get_repeating_list_for_section(self, section_id):
        return self.get_repeat_for_section(section_id).get("for_list")

    def get_repeating_title_for_section(self, section_id):
        return self.get_repeat_for_section(section_id).get("title")

    def get_repeating_page_title_for_section(self, section_id):
        return self.get_repeat_for_section(section_id).get("page_title")

    def get_custom_page_title_for_section(self, section_id):
        return self.get_summary_for_section(section_id).get("page_title")

    def get_section_for_block_id(self, block_id):
        block = self.get_block(block_id)

        if block.get("type") in LIST_COLLECTOR_CHILDREN + RELATIONSHIP_CHILDREN:
            section_id = self._get_parent_section_id_for_block(block_id)
        else:
            group_id = self._parent_id_map[block_id]
            section_id = self._parent_id_map[group_id]

        return self.get_section(section_id)

    def get_section_id_for_block_id(self, block_id):
        section = self.get_section_for_block_id(block_id)
        return section["id"]

    def get_groups(self):
        return self._groups_by_id.values()

    def get_group(self, group_id: str) -> Union[str, None]:
        return self._groups_by_id.get(group_id)

    def get_group_for_block_id(self, block_id: str) -> Union[str, None]:
        return self._group_for_block(block_id)

    def get_last_block_id_for_section(self, section_id):
        section = self.get_section(section_id)
        if section:
            return section["groups"][-1]["blocks"][-1]["id"]

    def get_first_block_id_for_group(self, group_id):
        group = self.get_group(group_id)
        if group:
            return group["blocks"][0]["id"]

    def get_first_block_id_for_section(self, section_id):
        section = self.get_section(section_id)
        if section:
            group_id = section["groups"][0]["id"]
            return self.get_first_block_id_for_group(group_id)

    def get_blocks(self):
        return self._blocks_by_id.values()

    def get_block(self, block_id):
        return self._blocks_by_id.get(block_id)

    def is_block_valid(self, block_id):
        return bool(self.get_block(block_id))

    def get_block_for_answer_id(self, answer_id):
        return self._block_for_answer(answer_id)

    def is_block_in_repeating_section(self, block_id):
        section_id = self.get_section_id_for_block_id(block_id=block_id)

        return self.get_repeating_list_for_section(section_id)

    def is_answer_in_list_collector_block(self, answer_id):
        block = self.get_block_for_answer_id(answer_id)

        return self.is_list_block_type(block["type"])

    def is_answer_in_repeating_section(self, answer_id):
        block = self.get_block_for_answer_id(answer_id)

        return self.is_block_in_repeating_section(block_id=block["id"])

    def get_list_item_id_for_answer_id(self, answer_id, list_item_id):
        if (
            list_item_id
            and not self.is_answer_in_list_collector_block(answer_id)
            and not self.is_answer_in_repeating_section(answer_id)
        ):
            return None

        return list_item_id

    def get_answers_by_answer_id(self, answer_id):
        """Return answers matching answer id, including all matching answers inside
        variants
        """
        return self._answers_by_id.get(answer_id)

    def get_default_answer(self, answer_id):
        try:
            answer_schema = self.get_answers_by_answer_id(answer_id)[0]
            answer = Answer(answer_schema["id"], answer_schema["default"])
        except (KeyError, TypeError):
            return None

        return answer

    def get_add_block_for_list_collector(self, list_collector_id):
        add_block_map = {
            "ListCollector": "add_block",
            "PrimaryPersonListCollector": "add_or_edit_block",
        }
        list_collector = self.get_block(list_collector_id)

        return list_collector[add_block_map[list_collector["type"]]]

    def get_answer_ids_for_list_items(self, list_collector_id):
        """
        Get answer ids used to add items to a list.
        """
        add_block = self.get_add_block_for_list_collector(list_collector_id)
        return self.get_answer_ids_for_block(add_block["id"])

    def get_questions(self, question_id):
        """Return a list of questions matching some question id
        This includes all questions inside variants
        """
        return self._questions_by_id.get(question_id)

    @staticmethod
    def get_list_collectors_for_list(section, for_list, primary=False):
        collector_type = "PrimaryPersonListCollector" if primary else "ListCollector"

        return (
            block
            for block in QuestionnaireSchema.get_blocks_for_section(section)
            if block["type"] == collector_type and block["for_list"] == for_list
        )

    @staticmethod
    def get_list_collector_for_list(section, for_list, primary=False):
        try:
            return next(
                QuestionnaireSchema.get_list_collectors_for_list(
                    section, for_list, primary
                )
            )
        except StopIteration:
            return None

    @classmethod
    def get_answer_ids_for_question(cls, question):
        answer_ids = []

        for answer in question.get("answers", []):
            answer_ids.append(answer["id"])
            for option in answer.get("options", []):
                if "detail_answer" in option:
                    answer_ids.append(option["detail_answer"]["id"])

        return answer_ids

    def get_first_answer_id_for_block(self, block_id):
        answer_ids = self.get_answer_ids_for_block(block_id)
        return answer_ids[0]

    def get_answer_ids_for_block(self, block_id):
        block = self.get_block(block_id)

        if block:
            if block.get("question"):
                return self.get_answer_ids_for_question(block["question"])
            if block.get("question_variants"):
                return self.get_answer_ids_for_question(
                    block["question_variants"][0]["question"]
                )
        return []

    def get_relationship_collectors(self) -> List:
        return [
            block
            for block in self.get_blocks()
            if block["type"] == "RelationshipCollector"
        ]

    def get_relationship_collectors_by_list_name(self, list_name: str):
        relationship_collectors = self.get_relationship_collectors()
        if relationship_collectors:
            return [
                block
                for block in relationship_collectors
                if block["for_list"] == list_name
            ]

    def get_unrelated_block_no_answer_values(self, unrelated_answer_id):
        return [
            option["value"]
            for unrelated_answer in self.get_answers_by_answer_id(unrelated_answer_id)
            for option in unrelated_answer["options"]
            if option.get("action", {}).get("type") == "AddUnrelatedRelationships"
        ]

    @staticmethod
    def get_single_string_value(schema_object):
        """
        Resolves an identifying string value for the schema_object. If text_plural the `other` form is returned.
        :return: string value
        """
        if isinstance(schema_object, dict):
            if "text_plural" in schema_object:
                return schema_object["text_plural"]["forms"]["other"]
            return schema_object["text"]
        return schema_object

    @staticmethod
    def get_all_questions_for_block(block):
        all_questions = []
        if block:
            if block.get("question"):
                all_questions.append(block["question"])
            elif block.get("question_variants"):
                for variant in block["question_variants"]:
                    all_questions.append(variant["question"])

            return all_questions
        return []

    @staticmethod
    def is_primary_person_block_type(block_type):
        primary_person_blocks = [
            "PrimaryPersonListCollector",
            "PrimaryPersonListAddOrEditQuestion",
        ]

        return block_type in primary_person_blocks

    @staticmethod
    def is_list_block_type(block_type):
        list_blocks = ["ListCollector"] + LIST_COLLECTOR_CHILDREN
        return block_type in list_blocks

    @staticmethod
    def is_question_block_type(block_type):
        return block_type in [
            "Question",
            "ListCollectorDrivingQuestion",
            "ConfirmationQuestion",
        ]

    @staticmethod
    def has_address_lookup_answer(question):
        return any(
            answer
            for answer in question["answers"]
            if answer["type"] == "Address" and "lookup_options" in answer
        )

    def _get_parent_section_id_for_block(self, block_id):
        parent_block_id = self._parent_id_map[block_id]
        group_id = self._parent_id_map[parent_block_id]
        section_id = self._parent_id_map[group_id]
        return section_id

    def _block_for_answer(self, answer_id):
        question_id = self._parent_id_map[answer_id]
        block_id = self._parent_id_map[question_id]
        parent_block_id = self._parent_id_map[block_id]
        parent_block = self.get_block(parent_block_id)

        if parent_block and parent_block["type"] == "ListCollector":
            return parent_block

        return self.get_block(block_id)

    def _group_for_block(self, block_id):
        block = self.get_block(block_id)
        parent_id = self._parent_id_map[block_id]
        if block["type"] in LIST_COLLECTOR_CHILDREN:
            group_id = self._parent_id_map[parent_id]
            return self.get_group(group_id)

        return self.get_group(parent_id)

    def _get_error_messages(self):
        # Force translation of global error messages (stored as LazyString's) into the language of the schema.
        with force_locale(self.language_code):
            messages = {k: str(v) for k, v in error_messages.items()}

        if "messages" in self.json:
            messages.update(self.json["messages"])

        return messages
