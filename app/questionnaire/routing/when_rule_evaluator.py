from dataclasses import dataclass
from datetime import date
from typing import Callable, Generator, Mapping, Optional, Sequence, Union

from app.data_models import AnswerStore, ListStore
from app.questionnaire import Location, QuestionnaireSchema
from app.questionnaire.relationship_location import RelationshipLocation
from app.questionnaire.routing.operations import Operations
from app.questionnaire.routing.operator import Operator
from app.questionnaire.value_source_resolver import (
    ValueSourceResolver,
    ValueSourceTypes,
)


@dataclass
class WhenRuleEvaluator:
    schema: QuestionnaireSchema
    answer_store: AnswerStore
    list_store: ListStore
    metadata: Mapping
    response_metadata: Mapping
    location: Union[None, Location, RelationshipLocation]
    routing_path_block_ids: Optional[list] = None

    # pylint: disable=attribute-defined-outside-init
    def __post_init__(self) -> None:
        list_item_id = self.location.list_item_id if self.location else None
        self.value_source_resolver = ValueSourceResolver(
            answer_store=self.answer_store,
            list_store=self.list_store,
            metadata=self.metadata,
            response_metadata=self.response_metadata,
            schema=self.schema,
            location=self.location,
            list_item_id=list_item_id,
            routing_path_block_ids=self.routing_path_block_ids,
            use_default_answer=True,
        )
        operations = Operations()
        self.operation_mapping: dict[str, Callable] = {
            Operator.NOT: operations.evaluate_not,
            Operator.AND: operations.evaluate_and,
            Operator.OR: operations.evaluate_or,
            Operator.EQUAL: operations.evaluate_equal,
            Operator.NOT_EQUAL: operations.evaluate_not_equal,
            Operator.GREATER_THAN: operations.evaluate_greater_than,
            Operator.LESS_THAN: operations.evaluate_less_than,
            Operator.GREATER_THAN_OR_EQUAL: operations.evaluate_greater_than_or_equal,
            Operator.LESS_THAN_OR_EQUAL: operations.evaluate_less_than_or_equal,
            Operator.IN: operations.evaluate_in,
            Operator.ALL_IN: operations.evaluate_all_in,
            Operator.ANY_IN: operations.evaluate_any_in,
            Operator.COUNT: operations.evaluate_count,
            Operator.DATE: operations.resolve_date_from_string,
        }

    def _evaluate(self, rule: dict[str, Sequence]) -> Union[bool, Optional[date]]:
        next_rule = next(iter(rule))
        operator = Operator(next_rule, self.operation_mapping[next_rule])
        operands = rule[next_rule]

        if not isinstance(rule[next_rule], Sequence):
            raise TypeError(
                f"The rule is invalid, operands should be of type Sequence and not {type(operands)}"
            )

        resolved_operands = self.get_resolved_operands(operands)
        return operator.evaluate(resolved_operands)

    def get_resolved_operands(
        self, operands: Sequence[ValueSourceTypes]
    ) -> Generator[Union[bool, Optional[date], ValueSourceTypes], None, None]:
        for operand in operands:
            if isinstance(operand, dict) and "source" in operand:
                yield self.value_source_resolver.resolve(operand)
            elif isinstance(operand, dict) and any(
                operator in operand for operator in self.operation_mapping
            ):
                yield self._evaluate(operand)
            else:
                yield operand

    def evaluate(self, rule: dict[str, Sequence]) -> Union[bool, Optional[date]]:
        return self._evaluate(rule)
