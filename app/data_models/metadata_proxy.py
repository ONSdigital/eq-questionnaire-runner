from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Mapping, Optional

from werkzeug.datastructures import ImmutableDict

from app.authentication.auth_payload_version import AuthPayloadVersion
from app.utilities.serialize import serialize

TOP_LEVEL_METADATA_KEYS = [
    "tx_id",
    "account_service_url",
    "case_id",
    "collection_exercise_sid",
    "response_id",
    "response_expires_at",
    "language_code",
    "schema_name",
    "schema_url",
    "channel",
    "region_code",
    "roles",
]


@dataclass(frozen=True)
class SurveyMetadata:
    data: ImmutableDict = field(default_factory=dict)  # type: ignore
    receipting_keys: Optional[tuple] = None

    def __getitem__(self, key: str) -> Optional[Any]:
        return self.data.get(key)


# pylint: disable=too-many-locals
@dataclass(frozen=True)
class MetadataProxy:
    tx_id: str
    account_service_url: str
    case_id: str
    collection_exercise_sid: str
    response_id: str
    survey_metadata: Optional[SurveyMetadata] = None
    schema_url: Optional[str] = None
    schema_name: Optional[str] = None
    language_code: Optional[str] = None
    response_expires_at: Optional[datetime] = None
    channel: Optional[str] = None
    region_code: Optional[str] = None
    version: Optional[AuthPayloadVersion] = None
    roles: Optional[list] = None

    def __getitem__(self, key: str) -> Optional[Any]:
        if self.survey_metadata and key in self.survey_metadata.data:
            return self.survey_metadata[key]

        return getattr(self, key, None)

    @classmethod
    def from_dict(cls, metadata: Mapping) -> MetadataProxy:
        _metadata = deepcopy(dict(metadata))
        version = _metadata.pop("version", None)

        if version == AuthPayloadVersion.V2.value:
            serialized_metadata = cls.serialize(_metadata.pop("survey_metadata", {}))
            survey_metadata = SurveyMetadata(**serialized_metadata)
        else:
            serialized_metadata = cls.serialize(_metadata)
            survey_metadata = SurveyMetadata(data=serialized_metadata)

        top_level_data = {
            key: _metadata.pop(key, None) for key in TOP_LEVEL_METADATA_KEYS
        }

        return cls(
            **top_level_data,
            version=version,
            survey_metadata=survey_metadata,
        )

    @classmethod
    def serialize(cls, data: Any) -> Any:
        return serialize(data)
