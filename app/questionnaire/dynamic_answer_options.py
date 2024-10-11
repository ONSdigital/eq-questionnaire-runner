from dataclasses import dataclass
from typing import Mapping, Union

from app.questionnaire.rules.evaluator import EvaluatorTypes
from app.questionnaire.rules.operator import Operator
from app.questionnaire.rules.rule_evaluator import RuleEvaluator
from app.questionnaire.value_source_resolver import (
    ValueSourceEscapedTypes,
    ValueSourceResolver,
    ValueSourceTypes,
)


@dataclass
class DynamicAnswerOptions:
    dynamic_options_schema: Mapping
    rule_evaluator: RuleEvaluator
    value_source_resolver: ValueSourceResolver

    def evaluate(self) -> tuple[dict[str, str], ...]:
        values = self.dynamic_options_schema["values"]
        resolved_values: Union[
            ValueSourceEscapedTypes, ValueSourceTypes, EvaluatorTypes
        ]

        if "source" in values:
            if values["source"] != "answers":
                raise NotImplementedError  # pragma: no cover

            resolved_values = self.value_source_resolver.resolve(values)
        else:
            resolved_values = self.rule_evaluator.evaluate(values)

        if not resolved_values:
            return ()

        resolved_labels = self.rule_evaluator.evaluate(
            {
                Operator.MAP: [
                    self.dynamic_options_schema["transform"],
                    resolved_values,
                ]
            }
        )

        return tuple(
            {"label": label, "value": value}  # type: ignore
            for label, value in zip(resolved_labels, resolved_values)  # type: ignore
        )
