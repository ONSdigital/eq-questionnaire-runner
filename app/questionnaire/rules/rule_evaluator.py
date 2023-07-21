from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Generator, Iterable, MutableMapping, Optional, Sequence, Union

from app.data_models import AnswerStore, ListStore, ProgressStore
from app.data_models.metadata_proxy import MetadataProxy
from app.questionnaire import QuestionnaireSchema
from app.questionnaire.placeholder_renderer import PlaceholderRenderer
from app.questionnaire.questionnaire_schema import DEFAULT_LANGUAGE_CODE
from app.questionnaire.rules.operations import Operations
from app.questionnaire.rules.operator import Operator
from app.questionnaire.value_source_resolver import (
    ValueSourceResolver,
    ValueSourceTypes,
)
from app.utilities.types import LocationType

RuleEvaluatorTypes = Union[
    bool, Optional[date], list[str], list[date], int, float, Decimal
]


@dataclass
class RuleEvaluator:
    schema: QuestionnaireSchema
    answer_store: AnswerStore
    list_store: ListStore
    metadata: MetadataProxy | None
    response_metadata: MutableMapping
    location: LocationType | None
    progress_store: ProgressStore
    routing_path_block_ids: Iterable | None = None
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
            progress_store=self.progress_store,
            use_default_answer=True,
        )

        renderer: PlaceholderRenderer = PlaceholderRenderer(
            language=self.language,
            answer_store=self.answer_store,
            list_store=self.list_store,
            metadata=self.metadata,
            response_metadata=self.response_metadata,
            schema=self.schema,
            location=self.location,
            progress_store=self.progress_store,
        )
        self.operations = Operations(
            language=self.language, schema=self.schema, renderer=renderer
        )

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

        if QuestionnaireSchema.has_operator(operand) and isinstance(operand, dict):
            return self._evaluate(operand)

        return operand

    def get_resolved_operands(
        self, operands: Sequence[ValueSourceTypes]
    ) -> Generator[Union[bool, Optional[date], ValueSourceTypes], None, None]:
        for operand in operands:
            yield self._resolve_operand(operand)

    def evaluate(self, rule: dict[str, Sequence]) -> RuleEvaluatorTypes:
        return self._evaluate(rule)
