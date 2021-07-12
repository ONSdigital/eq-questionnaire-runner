from dataclasses import dataclass
from typing import Optional

from flask_babel.speaklater import LazyString


@dataclass
class Link:
    text: LazyString
    url: str
    target: Optional[str] = "_blank"
