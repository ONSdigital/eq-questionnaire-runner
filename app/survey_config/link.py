from dataclasses import dataclass, field
from typing import Optional

from flask_babel.speaklater import LazyString


@dataclass
class Link:
    text: LazyString
    url: str
    target: Optional[str] = "_blank"


@dataclass
class HeaderLink:
    title: LazyString
    url: str
    id: str


@dataclass
class SummaryLink:
    text: LazyString
    url: str
    attributes: Optional[dict] = field(default_factory=dict)
    target: Optional[str] = "_self"
