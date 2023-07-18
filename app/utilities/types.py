from collections import namedtuple
from typing import TypeAlias

from app.questionnaire.location import Location
from app.questionnaire.relationship_location import RelationshipLocation

LocationType: TypeAlias = Location | RelationshipLocation

SectionKey = namedtuple("SectionKey", "section_id list_item_id")
