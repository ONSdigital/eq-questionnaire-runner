from dataclasses import dataclass
from datetime import date
from typing import Generator, Mapping, Optional, Sequence, Union

from app.data_models import AnswerStore, ListStore
from app.questionnaire import Location, QuestionnaireSchema
from app.questionnaire.relationship_location import RelationshipLocation
from app.questionnaire.routing.operator import OPERATIONS_MAPPINGS, Operator
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

    def _evaluate(self, rule: dict[str, Sequence]) -> Union[bool, Optional[date]]:
        operator = Operator(next(iter(rule)))
        operands = rule[operator.name]

        if not isinstance(operands, Sequence):
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
                operator in operand for operator in OPERATIONS_MAPPINGS
            ):
                yield self._evaluate(operand)
            else:
                yield operand

    def evaluate(self, rule: dict[str, Sequence]) -> Union[bool, Optional[date]]:
        return self._evaluate(rule)
