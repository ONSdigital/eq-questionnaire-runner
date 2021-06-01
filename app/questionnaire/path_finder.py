from typing import List, Mapping, Optional

from app.data_models.answer_store import AnswerStore
from app.data_models.list_store import ListStore
from app.data_models.progress_store import ProgressStore
from app.questionnaire.location import Location
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.questionnaire.routing_path import RoutingPath
from app.questionnaire.rules import (
    evaluate_goto,
    evaluate_skip_conditions,
    is_goto_rule,
)


class PathFinder:
    def __init__(
        self,
        schema: QuestionnaireSchema,
        answer_store: AnswerStore,
        list_store: ListStore,
        progress_store: ProgressStore,
        metadata: Mapping,
    ):
        self.answer_store = answer_store
        self.metadata = metadata
        self.schema = schema
        self.progress_store = progress_store
        self.list_store = list_store

    def routing_path(
        self, section_id: str, list_item_id: Optional[str] = None
    ) -> RoutingPath:
        """
        Visits all the blocks in a section and returns a path given a list of answers.
        """
        blocks: List[Mapping] = []
        routing_path_block_ids = []
        current_location = Location(section_id=section_id, list_item_id=list_item_id)
        section = self.schema.get_section(section_id)
        list_name = self.schema.get_repeating_list_for_section(
            current_location.section_id
        )

        if section:
            for group in section["groups"]:
                if "skip_conditions" in group:
                    if evaluate_skip_conditions(
                        group["skip_conditions"],
                        self.schema,
                        self.metadata,
                        self.answer_store,
                        self.list_store,
                        current_location=current_location,
                    ):
                        continue

                blocks.extend(group["blocks"])

        if blocks:
            routing_path_block_ids = self._build_routing_path_block_ids(
                blocks, current_location
            )

        return RoutingPath(routing_path_block_ids, section_id, list_item_id, list_name)

    @staticmethod
    def _block_index_for_block_id(blocks, block_id):
        return next(
            (index for (index, block) in enumerate(blocks) if block["id"] == block_id),
            None,
        )

    def _build_routing_path_block_ids(self, blocks, current_location):
        # Keep going unless we've hit the last block
        routing_path_block_ids = []
        block_index = 0
        repeating_list = self.schema.get_repeating_list_for_section(
            current_location.section_id
        )

        while block_index < len(blocks):
            block = blocks[block_index]

            is_skipping = block.get("skip_conditions") and evaluate_skip_conditions(
                block["skip_conditions"],
                self.schema,
                self.metadata,
                self.answer_store,
                self.list_store,
                current_location=current_location,
                routing_path_block_ids=routing_path_block_ids,
            )

            if not is_skipping:
                block_id = block["id"]
                if repeating_list and current_location.list_item_id:
                    this_location = Location(
                        section_id=current_location.section_id,
                        block_id=block_id,
                        list_name=repeating_list,
                        list_item_id=current_location.list_item_id,
                    )
                else:
                    this_location = Location(
                        section_id=current_location.section_id, block_id=block_id
                    )

                if block_id not in routing_path_block_ids:
                    routing_path_block_ids.append(block_id)

                # If routing rules exist then a rule must match (i.e. default goto)
                routing_rules = block.get("routing_rules")
                if routing_rules:
                    block_index = self._evaluate_routing_rules(
                        this_location,
                        blocks,
                        routing_rules,
                        block_index,
                        routing_path_block_ids,
                    )
                    if block_index:
                        continue

                    return routing_path_block_ids

            # Last block so return routing_path_block_ids
            if block_index == len(blocks) - 1:
                return routing_path_block_ids

            # No routing rules, so step forward a block
            block_index = block_index + 1

    def _evaluate_routing_rules(
        self, this_location, blocks, routing_rules, block_index, routing_path_block_ids
    ):
        for rule in filter(is_goto_rule, routing_rules):
            should_goto = evaluate_goto(
                rule["goto"],
                self.schema,
                self.metadata,
                self.answer_store,
                self.list_store,
                current_location=this_location,
                routing_path_block_ids=routing_path_block_ids,
            )

            if should_goto:
                if rule["goto"].get("section") == "End":
                    return None

                next_block_id = self._get_next_block_id(rule)
                next_block_index = PathFinder._block_index_for_block_id(
                    blocks, next_block_id
                )
                next_precedes_current = (
                    next_block_index is not None and next_block_index < block_index
                )

                if next_precedes_current:
                    self._remove_rule_answers(rule["goto"], this_location)
                    routing_path_block_ids.append(next_block_id)
                    return None

                return next_block_index

    def _get_next_block_id(self, rule):
        if "group" in rule["goto"]:
            return self.schema.get_first_block_id_for_group(rule["goto"]["group"])
        return rule["goto"]["block"]

    def _remove_rule_answers(self, goto_rule, this_location):
        # We're jumping backwards, so need to delete all answers from which
        # route is derived. Need to filter out conditions that don't use answers
        if "when" in goto_rule.keys():
            for condition in goto_rule["when"]:
                if "meta" not in condition.keys():
                    self.answer_store.remove_answer(condition["id"])

        self.progress_store.remove_completed_location(location=this_location)
