from dataclasses import dataclass
from typing import Any, Mapping

from app.questionnaire.rules.operator import Operator
from app.questionnaire.rules.rule_evaluator import RuleEvaluator


@dataclass
class DynamicAnswerOptions:
    dynamic_options_schema: Mapping[str, Any]
    rule_evaluator: RuleEvaluator

    def evaluate(self) -> tuple[dict[str, str], ...]:
        values = self.dynamic_options_schema["values"]
        if "source" in values:  # pylint: disable=no-else-raise
            # :TODO: Implement value sources support
            # resolved_values = ...
            raise NotImplementedError  # pragma: no cover
        else:
            resolved_values = self.rule_evaluator.evaluate(values)

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
