from typing import List, Mapping, Optional

from app.data_models.answer_store import AnswerStore
from app.data_models.list_store import ListStore
from app.data_models.progress_store import CompletionStatus, ProgressStore
from app.questionnaire.location import Location
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.questionnaire.routing_path import RoutingPath
from app.questionnaire.rules.operator import OPERATION_MAPPING
from app.questionnaire.rules.rule_evaluator import RuleEvaluator
from app.questionnaire.when_rules import evaluate_goto, evaluate_when_rules


class PathFinder:
    def __init__(
        self,
        schema: QuestionnaireSchema,
        answer_store: AnswerStore,
        list_store: ListStore,
        progress_store: ProgressStore,
        metadata: Mapping,
        response_metadata: Mapping,
    ):
        self.answer_store = answer_store
        self.metadata = metadata
        self.response_metadata = response_metadata
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
        routing_path_block_ids: List[str] = []
        current_location = Location(section_id=section_id, list_item_id=list_item_id)
        section = self.schema.get_section(section_id)
        list_name = self.schema.get_repeating_list_for_section(
            current_location.section_id
        )

        if section:
            for group in section["groups"]:
                if "skip_conditions" in group:
                    skip_conditions = group.get("skip_conditions")
                    if self.evaluate_skip_conditions(
                        current_location, routing_path_block_ids, skip_conditions
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
            skip_conditions = block.get("skip_conditions")
            is_skipping = self.evaluate_skip_conditions(
                current_location, routing_path_block_ids, skip_conditions
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
        when_rule_evaluator = RuleEvaluator(
            self.schema,
            self.answer_store,
            self.list_store,
            self.metadata,
            self.response_metadata,
            location=this_location,
            routing_path_block_ids=routing_path_block_ids,
        )
        for rule in routing_rules:
            if "goto" in rule:
                rule = rule["goto"]
                should_goto = evaluate_goto(
                    rule,
                    self.schema,
                    self.metadata,
                    self.answer_store,
                    self.list_store,
                    current_location=this_location,
                    routing_path_block_ids=routing_path_block_ids,
                )
            else:
                should_goto = should_goto_new(rule, when_rule_evaluator)

            if should_goto:
                if rule.get("section") == "End":
                    return None

                next_block_id = self._get_next_block_id(rule)
                next_block_index = PathFinder._block_index_for_block_id(
                    blocks, next_block_id
                )
                next_precedes_current = (
                    next_block_index is not None and next_block_index < block_index
                )

                if next_precedes_current:
                    self._remove_current_blocks_answers_for_backwards_routing(
                        rule, this_location
                    )
                    routing_path_block_ids.append(next_block_id)
                    return None

                return next_block_index

    def evaluate_skip_conditions(
        self, this_location, routing_path_block_ids, skip_conditions
    ):
        if not skip_conditions:
            return False

        if isinstance(skip_conditions, dict):
            when_rule_evaluator = RuleEvaluator(
                self.schema,
                self.answer_store,
                self.list_store,
                self.metadata,
                self.response_metadata,
                location=this_location,
                routing_path_block_ids=routing_path_block_ids,
            )

            return when_rule_evaluator.evaluate(skip_conditions["when"])

        for when in skip_conditions:
            condition = evaluate_when_rules(
                when["when"],
                self.schema,
                self.metadata,
                self.answer_store,
                self.list_store,
                current_location=this_location,
                routing_path_block_ids=routing_path_block_ids,
            )
            if condition is True:
                return True
        return False

    def _get_next_block_id(self, rule):
        if "group" in rule:
            return self.schema.get_first_block_id_for_group(rule["group"])
        return rule["block"]

    def _remove_current_blocks_answers_for_backwards_routing(
        self, rules: dict, this_location: Location
    ) -> None:

        if block_id := this_location.block_id:
            answer_ids_for_current_block = self.schema.get_answer_ids_for_block(
                block_id
            )
            if "when" in rules:
                if isinstance(rules["when"], dict):
                    self._remove_current_blocks_answers_for_new_backwards_routing(
                        rules["when"], answer_ids_for_current_block
                    )
                else:
                    for rule in rules["when"]:
                        if "id" in rule and rule["id"] in answer_ids_for_current_block:
                            self.answer_store.remove_answer(rule["id"])

            self.progress_store.remove_location_for_backwards_routing(this_location)
            self.progress_store.update_section_status(
                CompletionStatus.IN_PROGRESS, this_location.section_id
            )

    def _remove_current_blocks_answers_for_new_backwards_routing(
        self, rules: dict, answer_ids_for_current_block: list[str]
    ) -> None:
        operands = self.schema.get_operands(rules)
        for rule in operands:
            if isinstance(rule, dict) and (
                "identifier" in rule
                and rule["identifier"] in answer_ids_for_current_block
            ):
                if (
                    "identifier" in rule
                    and rule["identifier"] in answer_ids_for_current_block
                ):
                    self.answer_store.remove_answer(rule["identifier"])
            if any(operator in rule for operator in OPERATION_MAPPING):
                return self._remove_current_blocks_answers_for_new_backwards_routing(
                    rule, answer_ids_for_current_block
                )


def should_goto_new(rule, when_rule_evaluator):
    if when_rule := rule.get("when"):
        return when_rule_evaluator.evaluate(when_rule)

    return True
