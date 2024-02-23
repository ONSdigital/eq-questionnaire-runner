from __future__ import annotations

from dataclasses import asdict, dataclass, field
from decimal import Decimal
from typing import Optional, TypedDict, Union, overload

from markupsafe import Markup, escape

DictAnswer = dict[str, Union[int, str]]
ListAnswer = list[str]
ListDictAnswer = list[DictAnswer]
DictAnswerEscaped = dict[str, Union[int, Markup]]
ListAnswerEscaped = list[Markup]
ListDictAnswerEscaped = list[DictAnswerEscaped]

AnswerValueTypes = Union[str, int, Decimal, DictAnswer, ListAnswer, ListDictAnswer]
AnswerValueEscapedTypes = Union[
    Markup, int, Decimal, DictAnswerEscaped, ListAnswerEscaped, ListDictAnswerEscaped
]


class AnswerDict(TypedDict, total=False):
    answer_id: str
    list_item_id: str
    value: AnswerValueTypes


@dataclass
class Answer:
    answer_id: str
    value: AnswerValueTypes
    list_item_id: Optional[str] = field(default=None)

    @classmethod
    def from_dict(cls, answer_dict: AnswerDict) -> Answer:
        return cls(
            answer_id=answer_dict["answer_id"],
            value=answer_dict["value"],
            list_item_id=answer_dict.get("list_item_id"),
        )

    def for_json(self) -> dict:
        output = self.to_dict()
        if not self.list_item_id:
            del output["list_item_id"]
        return output

    def to_dict(self) -> dict:
        return asdict(self)


@overload
def escape_answer_value(value: ListAnswer) -> ListAnswerEscaped: ...  # pragma: no cover


@overload
def escape_answer_value(value: DictAnswer) -> DictAnswerEscaped: ...  # pragma: no cover


@overload
def escape_answer_value(
    value: ListDictAnswer,
) -> ListDictAnswerEscaped: ...  # pragma: no cover


@overload
def escape_answer_value(value: str) -> Markup: ...  # pragma: no cover


@overload
def escape_answer_value(
    value: Union[None, int, Decimal]
) -> Union[None, int, Decimal]: ...  # pragma: no cover


def escape_answer_value(
    value: Optional[AnswerValueTypes],
) -> Optional[AnswerValueEscapedTypes]:
    if isinstance(value, list):
        return [escape(item) for item in value]

    if isinstance(value, dict):
        return {
            key: escape(val) if isinstance(val, str) else val
            for key, val in value.items()
        }

    return escape(value) if isinstance(value, str) else value
