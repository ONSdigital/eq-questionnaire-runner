from typing import Mapping, Optional

from werkzeug.datastructures import ImmutableDict

from app.data_models.answer_store import AnswerStore
from app.data_models.list_store import ListStore
from app.data_models.metadata_proxy import MetadataProxy
from app.data_models.progress_store import CompletionStatus, ProgressStore
from app.questionnaire.location import Location
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.questionnaire.routing_path import RoutingPath
from app.questionnaire.rules.rule_evaluator import RuleEvaluator, RuleEvaluatorTypes


class PathFinder:
    def __init__(
        self,
        schema: QuestionnaireSchema,
        answer_store: AnswerStore,
        list_store: ListStore,
        progress_store: ProgressStore,
        metadata: Optional[MetadataProxy],
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
        routing_path_block_ids: list[str] = []
        current_location = Location(section_id=section_id, list_item_id=list_item_id)
        section = self.schema.get_section(section_id)
        list_name = self.schema.get_repeating_list_for_section(
            current_location.section_id
        )

        if section:
            when_rules_block_dependencies = self.get_when_rules_block_dependencies(
                section["id"]
            )
            blocks = self._get_not_skipped_blocks_in_section(
                current_location,
                routing_path_block_ids,
                section,
                when_rules_block_dependencies,
            )

            if blocks:
                routing_path_block_ids = self._build_routing_path_block_ids(
                    blocks, current_location, when_rules_block_dependencies
                )

        return RoutingPath(routing_path_block_ids, section_id, list_item_id, list_name)

    def get_when_rules_block_dependencies(self, section_id: str) -> list[str]:
        """NB: At present when rules block dependencies does not fully support repeating sections.
        It is supported when the section is dependent i.e the current section is repeating and building the routing path for sections that are not,
        It isn't supported if it needs to build the path for repeating sections"""
        return [
            block_id
            for dependent_section in self.schema.when_rules_section_dependencies_by_section.get(
                section_id, {}
            )
            for block_id in self.routing_path(dependent_section)
            if (dependent_section, None) in self.progress_store.started_section_keys()
        ]

    def _get_not_skipped_blocks_in_section(
        self,
        location: Location,
        routing_path_block_ids: list[str],
        section: ImmutableDict,
        when_rules_block_dependencies: list[str],
    ) -> Optional[list[Mapping]]:
        # :TODO: Fix group skipping in its own section. Routing path will be empty and therefore not checked
        if section:
            not_skipped_blocks: list[Mapping] = []
            for group in section["groups"]:
                if "skip_conditions" in group:
                    skip_conditions = group.get("skip_conditions")
                    if self.evaluate_skip_conditions(
                        location,
                        routing_path_block_ids,
                        skip_conditions,
                        when_rules_block_dependencies,
                    ):
                        continue
                not_skipped_blocks.extend(group["blocks"])

            return not_skipped_blocks

    @staticmethod
    def _block_index_for_block_id(blocks: dict, block_id: str) -> int | None: #TODO check 
        return next(
            (index for (index, block) in enumerate(blocks) if block["id"] == block_id),
            None,
        )

    def _build_routing_path_block_ids(
        self,
        blocks: list[Mapping],
        current_location: Location,
        when_rules_block_dependencies: list[str],
    ) -> list[str]:
        # Keep going unless we've hit the last block

        routing_path_block_ids: list[str] = []
        block_index = 0
        repeating_list = self.schema.get_repeating_list_for_section(
            current_location.section_id
        )

        while block_index < len(blocks):
            block = blocks[block_index]
            skip_conditions = block.get("skip_conditions")

            is_skipping = self.evaluate_skip_conditions(
                current_location,
                routing_path_block_ids,
                skip_conditions,
                when_rules_block_dependencies,
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
                        when_rules_block_dependencies,
                    )
                    if block_index:
                        continue

                    return routing_path_block_ids

            # Last block so return routing_path_block_ids
            if block_index == len(blocks) - 1:
                return routing_path_block_ids

            # No routing rules, so step forward a block
            block_index = block_index + 1

        return routing_path_block_ids  # pragma: no cover

    def _evaluate_routing_rules(
        self,
        this_location,
        blocks,
        routing_rules,
        block_index,
        routing_path_block_ids,
        when_rules_block_dependencies,
    ) -> int | None:
        if when_rules_block_dependencies:
            routing_path_block_ids = (
                when_rules_block_dependencies + routing_path_block_ids
            )

        when_rule_evaluator = RuleEvaluator(
            self.schema,
            self.answer_store,
            self.list_store,
            self.metadata,
            self.response_metadata,
            location=this_location,
            routing_path_block_ids=routing_path_block_ids,
            progress_store=self.progress_store,
        )
        for rule in routing_rules:
            rule_valid = (
                when_rule_evaluator.evaluate(when_rule)
                if (when_rule := rule.get("when"))
                else True
            )

            if rule_valid:
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
        self,
        this_location,
        routing_path_block_ids,
        skip_conditions,
        when_rules_block_dependencies,
    ) -> RuleEvaluatorTypes:
        if not skip_conditions:
            return False

        if when_rules_block_dependencies:
            routing_path_block_ids = (
                when_rules_block_dependencies + routing_path_block_ids
            )

        when_rule_evaluator = RuleEvaluator(
            schema=self.schema,
            answer_store=self.answer_store,
            list_store=self.list_store,
            metadata=self.metadata,
            response_metadata=self.response_metadata,
            progress_store=self.progress_store,
            location=this_location,
            routing_path_block_ids=routing_path_block_ids,
        )

        return when_rule_evaluator.evaluate(skip_conditions["when"])

    def _get_next_block_id(self, rule):
        if "group" in rule:
            return self.schema.get_first_block_id_for_group(rule["group"])
        return rule["block"]

    def _remove_current_blocks_answers_for_backwards_routing(
        self, rule: dict, this_location: Location
    ) -> None:
        if block_id := this_location.block_id:
            answer_ids_for_current_block = self.schema.get_answer_ids_for_block(
                block_id
            )
            if "when" in rule:
                self._remove_block_anwers_for_backward_routing_according_to_when_rule(
                    rule["when"], answer_ids_for_current_block
                )

            self.progress_store.remove_location_for_backwards_routing(this_location)
            self.progress_store.update_section_status(
                CompletionStatus.IN_PROGRESS, this_location.section_id
            )

    def _remove_block_anwers_for_backward_routing_according_to_when_rule(
        self, rules: dict, answer_ids_for_current_block: list[str]
    ) -> None:
        operands = self.schema.get_operands(rules)

        for rule in operands:
            if isinstance(rule, dict) and (
                "identifier" in rule
                and rule["identifier"] in answer_ids_for_current_block
            ):
                self.answer_store.remove_answer(rule["identifier"])

            if QuestionnaireSchema.has_operator(rule):
                return self._remove_block_anwers_for_backward_routing_according_to_when_rule(
                    rule, answer_ids_for_current_block
                )
