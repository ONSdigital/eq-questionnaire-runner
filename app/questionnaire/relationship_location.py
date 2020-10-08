from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from flask import url_for


@dataclass
class RelationshipLocation:
    section_id: str
    block_id: str
    list_item_id: str
    to_list_item_id: str
    list_name: str

    def for_json(self) -> Mapping:
        attributes = vars(self)
        return {k: v for k, v in attributes.items() if v is not None}

    def url(self, **kwargs) -> str:
        return url_for(
            "questionnaire.relationships",
            list_name=self.list_name,
            list_item_id=self.list_item_id,
            to_list_item_id=self.to_list_item_id,
            **kwargs,
        )
