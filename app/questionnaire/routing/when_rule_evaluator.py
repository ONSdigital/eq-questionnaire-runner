from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Union

from app.data_models import AnswerStore, ListStore
from app.questionnaire import Location, QuestionnaireSchema
from app.questionnaire.relationship_location import RelationshipLocation
from app.questionnaire.routing.operator import Operator
from app.questionnaire.value_source_resolver import (
    ValueSourceResolver,
    answer_value_types,
)


@dataclass
class WhenRuleEvaluator:
    rule: dict
    schema: QuestionnaireSchema
    answer_store: AnswerStore
    list_store: ListStore
    metadata: dict
    location: Union[Location, RelationshipLocation]
    routing_path_block_ids: Optional[list] = None

    def __post_init__(self) -> None:
        self.value_source_resolver = ValueSourceResolver(
            answer_store=self.answer_store,
            list_store=self.list_store,
            metadata=self.metadata,
            schema=self.schema,
            location=self.location,
            list_item_id=self.location.list_item_id,
            routing_path_block_ids=self.routing_path_block_ids,
            use_default_answer=True,
        )

    @staticmethod
    def _is_date_offset(rule: dict) -> bool:
        return any(x in rule for x in {"days", "months", "years"})

    def _evaluate(
        self, rule: answer_value_types
    ) -> Union[bool, datetime, answer_value_types]:
        if not isinstance(rule, dict) or self._is_date_offset(rule):
            return rule

        if "source" in rule:
            return self.value_source_resolver.resolve(rule)

        operator = Operator(next(iter(rule)))
        operands = rule[operator.name]

        if not isinstance(operands, (list, tuple)):
            raise TypeError(
                f"The rule is invalid. Got a non list/tuple for operands - {type(operands)}"
            )

        operands = (self._evaluate(operand) for operand in operands)
        return operator.evaluate(operands)

    def evaluate(self) -> Union[bool, datetime, answer_value_types]:
        return self._evaluate(self.rule)
