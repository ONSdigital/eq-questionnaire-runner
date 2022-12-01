from typing import Any, Mapping

from flask import url_for

from app.data_models.list_store import ListModel
from app.questionnaire import Location, QuestionnaireSchema
from app.questionnaire.placeholder_renderer import PlaceholderRenderer
from app.questionnaire.variants import choose_variant
from app.views import contexts
from app.views.contexts.summary.block import Block


class ListCollectorBlock:
    def __init__(
        self,
        routing_path,
        answer_store,
        list_store,
        progress_store,
        metadata,
        response_metadata,
        schema,
        location,
        language,
    ):
        self._location = location
        self._placeholder_renderer = PlaceholderRenderer(
            language=language,
            answer_store=answer_store,
            list_store=list_store,
            metadata=metadata,
            response_metadata=response_metadata,
            schema=schema,
        )
        self._list_store = list_store
        self._schema = schema
        self._location = location
        self._section = self._schema.get_section(self._location.section_id)
        self._language = language
        self._answer_store = answer_store
        self._metadata = metadata
        self._response_metadata = response_metadata
        self._routing_path = routing_path
        self._progress_store = progress_store

    # pylint: disable=too-many-locals
    def list_summary_element(self, summary: dict[str, str]) -> Mapping[str, Any]:
        list_collector_block = None
        (
            edit_block_id,
            remove_block_id,
            primary_person_edit_block_id,
            related_answers,
            answer_title,
            answer_focus,
        ) = (None, None, None, None, None, None)
        current_list = self._list_store[summary["for_list"]]

        list_collector_blocks = list(
            self._schema.get_list_collectors_for_list(
                self._section, for_list=summary["for_list"]
            )
        )

        add_link = self._add_link(summary, list_collector_block)

        list_collector_blocks_on_path = [
            list_collector_block
            for list_collector_block in list_collector_blocks
            if list_collector_block["id"] in self._routing_path.block_ids
        ]

        list_collector_block = (
            list_collector_blocks_on_path[0]
            if list_collector_blocks_on_path
            else list_collector_blocks[0]
        )

        rendered_summary = self._placeholder_renderer.render(
            summary, self._location.list_item_id
        )

        if list_collector_blocks_on_path:

            edit_block_id = list_collector_block["edit_block"]["id"]
            remove_block_id = list_collector_block["remove_block"]["id"]
            add_link = self._add_link(summary, list_collector_block)

        if len(current_list) == 1 and current_list.primary_person:

            if primary_person_block := self._schema.get_list_collector_for_list(
                self._section, for_list=summary["for_list"], primary=True
            ):
                primary_person_edit_block_id = edit_block_id = primary_person_block[
                    "add_or_edit_block"
                ]["id"]

        list_summary_context = self.list_context(
            list_collector_block["summary"],
            for_list=list_collector_block["for_list"],
            return_to="section-summary",
            edit_block_id=edit_block_id,
            remove_block_id=remove_block_id,
            primary_person_edit_block_id=primary_person_edit_block_id,
        )

        related_answers = (
            self._get_related_answers(current_list, list_collector_block.get("id"))
            if current_list
            else None
        )

        if related_answers:
            answer_focus = f"#{self._get_answer_id(list_collector_block)}"

        answer_title = (
            self._get_answer_title(list_collector_block) if related_answers else None
        )

        return {
            "title": rendered_summary["title"],
            "type": rendered_summary["type"],
            "add_link": add_link,
            "add_link_text": rendered_summary["add_link_text"],
            "empty_list_text": rendered_summary.get("empty_list_text"),
            "list_name": rendered_summary["for_list"],
            "related_answers": related_answers,
            "answer_title": answer_title,
            "answer_focus": answer_focus,
            **list_summary_context,
        }

    @property
    def list_context(self):
        return contexts.ListContext(
            self._language,
            self._schema,
            self._answer_store,
            self._list_store,
            self._progress_store,
            self._metadata,
            self._response_metadata,
        )

    def _add_link(self, summary, list_collector_block):

        if list_collector_block:
            return url_for(
                "questionnaire.block",
                list_name=summary["for_list"],
                block_id=list_collector_block["add_block"]["id"],
                return_to="section-summary",
            )

        driving_question_block = QuestionnaireSchema.get_driving_question_for_list(
            self._section, summary["for_list"]
        )

        if driving_question_block:
            return url_for(
                "questionnaire.block",
                block_id=driving_question_block["id"],
                return_to="section-summary",
            )

    def _get_related_answers(
        self, current_list: ListModel, list_collector_block_id
    ) -> dict[str, list]:
        section = self._section["id"]

        if related_answers := self._schema.get_related_answers_for_section(  # pylint: disable=too-many-nested-blocks
            section, current_list
        ):
            related_answers_dict = {}

            for list_id in current_list:
                for group in self._section.get("groups"):
                    for block in group.get("blocks"):

                        if block["type"] in ["ListCollector"]:
                            block_schema = {
                                "id": None,
                                "title": None,
                                "number": None,
                                "type": block["type"],
                                "for_list": current_list.name,
                                "question": None,
                            }
                            add_block = block.get("add_block")
                            question = add_block.get("question")
                            for answer in question.get("answers"):
                                if answer["id"] in related_answers:
                                    edit_block = (
                                        self._schema.get_edit_block_for_list_collector(
                                            list_collector_block_id
                                        )
                                    )
                                    edit_block_id = (
                                        edit_block.get("id") if edit_block else None
                                    )
                                    block_schema = dict(block_schema)
                                    block_schema["id"] = edit_block_id
                                    question = dict(question)
                                    answers = [
                                        answer
                                        for answer in question.get("answers")
                                        if answer["id"] in related_answers
                                    ]
                                    del question["answers"]
                                    question["answers"] = answers
                                    block_schema["question"] = question

                                    block = [
                                        Block(
                                            block_schema,
                                            answer_store=self._answer_store,
                                            list_store=self._list_store,
                                            metadata=self._metadata,
                                            response_metadata=self._response_metadata,
                                            schema=self._schema,
                                            location=Location(
                                                list_name=current_list.name,
                                                list_item_id=list_id,
                                                section_id=self._section["id"],
                                            ),
                                            return_to="section-summary",
                                            return_to_block_id=None,
                                        ).serialize()
                                    ]

                                    related_answers_dict[list_id] = block

            return related_answers_dict

    def _get_answer_title(self, list_collector_block: Mapping[str, Any]) -> str:
        if list_collector_block["add_block"].get("question_variants"):
            variant_label = choose_variant(
                list_collector_block["add_block"],
                self._schema,
                self._metadata,
                self._response_metadata,
                self._answer_store,
                self._list_store,
                variants_key="question_variants",
                single_key="question",
                current_location=self._location,
            )["answers"][0]["label"]

            return variant_label

        return list_collector_block["add_block"]["question"]["answers"][0]["label"]

    def _get_answer_id(self, list_collector_block: Mapping[str, Any]) -> str:
        if list_collector_block["add_block"].get("question_variants"):
            variant_label = choose_variant(
                list_collector_block["add_block"],
                self._schema,
                self._metadata,
                self._response_metadata,
                self._answer_store,
                self._list_store,
                variants_key="question_variants",
                single_key="question",
                current_location=self._location,
            )["answers"][0]["id"]

            return variant_label

        return list_collector_block["add_block"]["question"]["answers"][0]["id"]
