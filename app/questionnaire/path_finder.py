from typing import Iterable, Mapping, Sequence

from werkzeug.datastructures import ImmutableDict

from app.data_models import CompletionStatus
from app.data_models.data_stores import DataStores
from app.questionnaire.location import Location, SectionKey
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.questionnaire.routing_path import RoutingPath
from app.questionnaire.rules.rule_evaluator import RuleEvaluator, RuleEvaluatorTypes
from app.utilities.types import LocationType


class PathFinder:
    def __init__(self, schema: QuestionnaireSchema, data_stores: DataStores):
        self.data_stores = data_stores
        self.schema = schema

    def routing_path(self, section_key: SectionKey) -> RoutingPath:
        """
        Visits all the blocks in a section and returns a path given a list of answers.
        """
        routing_path_block_ids: list[str] = []
        current_location = Location(**section_key.to_dict())
        section = self.schema.get_section(section_key.section_id)
        list_name = self.schema.get_repeating_list_for_section(
            current_location.section_id
        )

        if section:
            when_rules_block_dependencies = self.get_when_rules_block_dependencies(
                section_key.section_id
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

        return RoutingPath(
            block_ids=routing_path_block_ids,
            list_name=list_name,
            **section_key.to_dict(),
        )

    def get_when_rules_block_dependencies(self, section_id: str) -> list[str]:
        """NB: At present when rules block dependencies does not fully support repeating sections.
        It is supported when the section is dependent i.e. the current section is repeating and building the routing path for sections that are not,
        It isn't supported if it needs to build the path for repeating sections"""
        dependencies_for_section = (
            self.schema.get_all_when_rules_section_dependencies_for_section(section_id)
        )

        return [
            block_id
            for dependent_section in dependencies_for_section
            for block_id in self.routing_path(SectionKey(dependent_section))
            if SectionKey(dependent_section)
            in self.data_stores.progress_store.started_section_keys()
        ]

    def _get_not_skipped_blocks_in_section(
        self,
        current_location: LocationType,
        routing_path_block_ids: list[str],
        section: ImmutableDict,
        when_rules_block_dependencies: list[str],
    ) -> list[dict] | None:
        # :TODO: Fix group skipping in its own section. Routing path will be empty and therefore not checked
        if section:
            not_skipped_blocks: list[dict] = []
            for group in section["groups"]:
                if "skip_conditions" in group:
                    skip_conditions = group.get("skip_conditions")
                    if self.evaluate_skip_conditions(
                        current_location,
                        routing_path_block_ids,
                        skip_conditions,
                        when_rules_block_dependencies,
                    ):
                        continue
                not_skipped_blocks.extend(group["blocks"])

            return not_skipped_blocks

    @staticmethod
    def _block_index_for_block_id(
        blocks: Iterable[Mapping], block_id: str
    ) -> int | None:
        return next(
            (index for (index, block) in enumerate(blocks) if block["id"] == block_id),
            None,
        )

    def _build_routing_path_block_ids(
        self,
        blocks: Sequence[Mapping],
        current_location: LocationType,
        when_rules_block_dependencies: list[str],
    ) -> list[str]:
        # Keep going unless we've hit the last block
        # routing_path_block_ids can be mutated by _evaluate_routing_rules
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
                routing_rules: Iterable[Mapping] | None = block.get("routing_rules")
                if routing_rules:
                    # Type ignore: block_index will always be non-null when evaluate is called
                    block_index = self._evaluate_routing_rules(  # type: ignore
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
        this_location: Location,
        blocks: Iterable[Mapping],
        routing_rules: Iterable[Mapping],
        block_index: int,
        routing_path_block_ids: list[str],
        when_rules_block_dependencies: list[str],
    ) -> int | None:
        # Use `list` to create a shallow copy since routing_path_block_ids is mutated hence we don't want to update its memory reference
        block_ids_for_dependencies = (
            list(routing_path_block_ids) + when_rules_block_dependencies
        )

        when_rule_evaluator = RuleEvaluator(
            self.schema,
            self.data_stores,
            location=this_location,
            routing_path_block_ids=block_ids_for_dependencies,
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
        current_location: LocationType,
        routing_path_block_ids: list[str],
        skip_conditions: ImmutableDict[str, dict] | None,
        when_rules_block_dependencies: list[str],
    ) -> RuleEvaluatorTypes:
        if not skip_conditions:
            return False

        block_ids_for_dependencies = (
            list(routing_path_block_ids) + when_rules_block_dependencies
        )

        when_rule_evaluator = RuleEvaluator(
            schema=self.schema,
            data_stores=self.data_stores,
            location=current_location,
            routing_path_block_ids=block_ids_for_dependencies,
        )

        return when_rule_evaluator.evaluate(skip_conditions["when"])

    def _get_next_block_id(self, rule: Mapping) -> str:
        if "group" in rule:
            # Type ignore: by this point the block for the rule will exist
            return self.schema.get_first_block_id_for_group(rule["group"])  # type: ignore
        # Type ignore: the rules block will be a string
        return rule["block"]  # type: ignore

    def _remove_current_blocks_answers_for_backwards_routing(
        self, rule: Mapping, this_location: Location
    ) -> None:
        if block_id := this_location.block_id:
            answer_ids_for_current_block = self.schema.get_answer_ids_for_block(
                block_id
            )
            if "when" in rule:
                self._remove_block_answers_for_backward_routing_according_to_when_rule(
                    rule["when"], answer_ids_for_current_block, this_location
                )

            self.data_stores.progress_store.remove_location_for_backwards_routing(
                this_location
            )
            self.data_stores.progress_store.update_section_status(
                CompletionStatus.IN_PROGRESS, this_location.section_key
            )

    def _remove_block_answers_for_backward_routing_according_to_when_rule(
        self,
        rules: Mapping,
        answer_ids_for_current_block: list[str],
        this_location: Location,
    ) -> None:
        operands = self.schema.get_operands(rules)

        for rule in operands:
            if isinstance(rule, dict) and (
                "identifier" in rule
                and rule["identifier"] in answer_ids_for_current_block
            ):
                self.data_stores.answer_store.remove_answer(
                    answer_id=rule["identifier"],
                    list_item_id=this_location.list_item_id,
                )

            if QuestionnaireSchema.has_operator(rule):
                return self._remove_block_answers_for_backward_routing_according_to_when_rule(
                    rule, answer_ids_for_current_block, this_location
                )
