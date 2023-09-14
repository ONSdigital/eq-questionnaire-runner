from dataclasses import dataclass
from typing import Any, Mapping

from flask import url_for

from app.questionnaire.location import SectionKey


@dataclass
class RelationshipLocation:
    section_id: str
    block_id: str
    list_name: str | None
    list_item_id: str | None
    to_list_item_id: str | None = None

    def for_json(self) -> Mapping:
        attributes = vars(self)
        return {k: v for k, v in attributes.items() if v is not None}

    def url(self, **kwargs: Any) -> str:
        if self.to_list_item_id:
            return url_for(
                "questionnaire.relationships",
                list_name=self.list_name,
                list_item_id=self.list_item_id,
                to_list_item_id=self.to_list_item_id,
                **kwargs,
            )
        return url_for(
            "questionnaire.relationships",
            list_name=self.list_name,
            list_item_id=self.list_item_id,
            block_id=self.block_id,
            **kwargs,
        )

    @property
    def section_key(self) -> SectionKey:
        return SectionKey(self.section_id, self.list_item_id)
