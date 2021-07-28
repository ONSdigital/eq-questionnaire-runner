from dataclasses import dataclass
from datetime import datetime
from typing import Generator, Optional, TypedDict, Union

from app.data_models import AnswerStore, ListStore
from app.questionnaire import Location, QuestionnaireSchema
from app.questionnaire.relationship_location import RelationshipLocation
from app.questionnaire.routing.operator import OPERATIONS, Operator
from app.questionnaire.value_source_resolver import (
    ValueSourceResolver,
    ValueSourceTypes,
)

DateOffset = TypedDict(
    "DateOffset", {"years": int, "months": int, "days": int}, total=False
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
    def _is_date_offset(rule: DateOffset) -> bool:
        return any(x in rule for x in {"days", "months", "years"})

    def _evaluate(self, rule: dict[str, list]) -> Union[bool, Optional[datetime]]:
        operator = Operator(next(iter(rule)))
        operands = rule[operator.name]

        if not isinstance(operands, list):
            raise TypeError(
                f"The rule is invalid. Got a non list type for operands - {type(operands)}"
            )

        resolved_operands = self.get_resolved_operands(operands)
        return operator.evaluate(resolved_operands)

    def get_resolved_operands(
        self, operands: list[ValueSourceTypes]
    ) -> Generator[Union[bool, Optional[datetime], ValueSourceTypes], None, None]:
        for operand in operands:
            if isinstance(operand, dict) and not self._is_date_offset(operand):
                if "source" in operand:
                    yield self.value_source_resolver.resolve(operand)
                elif any(operator in operand for operator in OPERATIONS):
                    yield self._evaluate(operand)
                else:
                    raise NotImplementedError("Got an unsupported operand")
            else:
                yield operand

    def evaluate(self) -> Union[bool, Optional[datetime]]:
        return self._evaluate(self.rule)
