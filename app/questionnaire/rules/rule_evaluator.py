from dataclasses import dataclass
from datetime import date
from typing import Generator, Iterable, Mapping, Optional, Sequence, Union

from app.data_models import AnswerStore, ListStore
from app.questionnaire import Location, QuestionnaireSchema
from app.questionnaire.questionnaire_schema import DEFAULT_LANGUAGE_CODE
from app.questionnaire.relationship_location import RelationshipLocation
from app.questionnaire.rules.operations import Operations
from app.questionnaire.rules.operator import OPERATION_MAPPING, Operator
from app.questionnaire.value_source_resolver import (
    ValueSourceResolver,
    ValueSourceTypes,
)


@dataclass
class RuleEvaluator:
    schema: QuestionnaireSchema
    answer_store: AnswerStore
    list_store: ListStore
    metadata: Mapping
    response_metadata: Mapping
    location: Union[None, Location, RelationshipLocation]
    routing_path_block_ids: Optional[list] = None
    language: str = DEFAULT_LANGUAGE_CODE

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
        self.operations = Operations(language=self.language)

    def _evaluate(self, rule: dict[str, Sequence]) -> Union[bool, Optional[date]]:
        operator_name = next(iter(rule))
        operator = Operator(operator_name, self.operations)
        operands = rule[operator_name]

        if not isinstance(operands, Sequence):
            raise TypeError(
                f"The rule is invalid, operands should be of type Sequence and not {type(operands)}"
            )

        resolved_operands: Iterable[Union[bool, Optional[date], ValueSourceTypes]]

        if operator_name == Operator.MAP:
            resolved_iterables = self._resolve_operand(operands[1])
            resolved_operands = [operands[0], resolved_iterables]
        else:
            resolved_operands = self.get_resolved_operands(operands)

        return operator.evaluate(resolved_operands)

    def _resolve_operand(
        self, operand: ValueSourceTypes
    ) -> Union[bool, Optional[date], ValueSourceTypes]:
        if isinstance(operand, dict) and "source" in operand:
            return self.value_source_resolver.resolve(operand)

        if isinstance(operand, dict) and any(
            operator in operand for operator in OPERATION_MAPPING
        ):
            return self._evaluate(operand)

        return operand

    def get_resolved_operands(
        self, operands: Sequence[ValueSourceTypes]
    ) -> Generator[Union[bool, Optional[date], ValueSourceTypes], None, None]:
        for operand in operands:
            yield self._resolve_operand(operand)

    def evaluate(
        self, rule: dict[str, Sequence]
    ) -> Union[bool, Optional[date], list[str], list[date]]:
        return self._evaluate(rule)
