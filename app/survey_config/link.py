from dataclasses import dataclass, field
from typing import Optional

from flask_babel.speaklater import LazyString


@dataclass
class Link:
    text: LazyString
    url: str
    target: Optional[str] = "_blank"
    attributes: Optional[dict] = field(default_factory=dict)

    def as_dict(self):
        return {k: v for k, v in self.__dict__.items() if v}


@dataclass
class HeaderLink:
    title: LazyString
    url: str
    id: str
