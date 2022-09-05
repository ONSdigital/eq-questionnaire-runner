from dataclasses import dataclass, field
from datetime import datetime
from typing import MutableMapping, Optional
from uuid import uuid4

from werkzeug.datastructures import ImmutableDict

from app.questionnaire import QuestionnaireSchema


@dataclass(frozen=True)
class SurveyMetadata:
    data: ImmutableDict = field(default_factory=dict)
    receipting_keys: Optional[tuple] = None

    def __getitem__(self, key):
        return getattr(self.data, key) if key in self.data else None


# pylint: disable=too-many-locals
@dataclass(frozen=True)
class MetadataProxy:
    tx_id: uuid4
    account_service_url: str
    case_id: uuid4
    collection_exercise_sid: uuid4
    response_id: str
    survey_metadata: SurveyMetadata = None
    schema_url: str = None
    schema_name: str = None
    language_code: str = None
    response_expires_at: Optional[datetime] = None
    channel: Optional[str] = None
    region_code: Optional[str] = None
    version: Optional[str] = None

    def __getitem__(self, key):
        if key in self.survey_metadata.data:
            return self.survey_metadata.data[key]
        return getattr(self, key, None)

    @classmethod
    def from_dict(cls, metadata: MutableMapping):
        tx_id = metadata.pop("tx_id")
        account_service_url = metadata.pop("account_service_url")
        case_id = metadata.pop("case_id")
        collection_exercise_sid = metadata.pop("collection_exercise_sid")
        response_id = metadata.pop("response_id")
        response_expires_at = metadata.pop("response_expires_at", None)
        language_code = metadata.pop("language_code", None)
        schema_name = metadata.pop("schema_name", None)
        schema_url = metadata.pop("schema_url", None)
        channel = metadata.pop("channel", None)
        region_code = metadata.pop("region_code", None)
        version = metadata.pop("version", None)

        if version == "v2":
            serialized_metadata: ImmutableDict = QuestionnaireSchema.serialize(
                metadata.pop("survey_metadata", {})
            )
            survey_metadata = SurveyMetadata(**serialized_metadata)
        else:
            serialized_metadata: ImmutableDict = QuestionnaireSchema.serialize(metadata)
            survey_metadata = SurveyMetadata(data=serialized_metadata)

        return cls(
            tx_id=tx_id,
            account_service_url=account_service_url,
            case_id=case_id,
            collection_exercise_sid=collection_exercise_sid,
            response_id=response_id,
            response_expires_at=response_expires_at,
            language_code=language_code,
            schema_name=schema_name,
            schema_url=schema_url,
            channel=channel,
            region_code=region_code,
            version=version,
            survey_metadata=survey_metadata,
        )
