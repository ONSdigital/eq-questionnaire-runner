from dataclasses import dataclass
from datetime import date
from typing import Generator, Optional, Union

from app.data_models import AnswerStore, ListStore
from app.questionnaire import Location, QuestionnaireSchema
from app.questionnaire.relationship_location import RelationshipLocation
from app.questionnaire.routing.operator import OPERATIONS, Operator
from app.questionnaire.value_source_resolver import (
    ValueSourceResolver,
    ValueSourceTypes,
)


@dataclass
class WhenRuleEvaluator:
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

    def _evaluate(
        self, rule: dict[str, Union[list, tuple]]
    ) -> Union[bool, Optional[date]]:
        operator = Operator(next(iter(rule)))
        operands = rule[operator.name]

        if not isinstance(operands, list) and not isinstance(operands, tuple):
            raise TypeError(
                f"The rule is invalid, operands should be of type list and not {type(operands)}"
            )

        resolved_operands = self.get_resolved_operands(operands)
        return operator.evaluate(resolved_operands)

    def get_resolved_operands(
        self, operands: Union[list[ValueSourceTypes], tuple]
    ) -> Generator[Union[bool, Optional[date], ValueSourceTypes], None, None]:
        for operand in operands:
            if isinstance(operand, dict) and "source" in operand:
                yield self.value_source_resolver.resolve(operand)
            elif isinstance(operand, dict) and any(
                operator in operand for operator in OPERATIONS
            ):
                yield self._evaluate(operand)
            else:
                yield operand

    def evaluate(
        self, rule: dict[str, Union[list, tuple]]
    ) -> Union[bool, Optional[date]]:
        return self._evaluate(rule)
