from datetime import datetime, timezone
from typing import Any

from marshmallow import Schema, fields, post_load, pre_dump


class QuestionnaireState:
    def __init__(
        self,
        user_id: str,
        state_data: str,
        collection_exercise_sid: str,
        version: int,
        submitted_at: datetime | None = None,
        expires_at: datetime | None = None,
    ):
        self.user_id = user_id
        self.state_data = state_data
        self.collection_exercise_sid = collection_exercise_sid
        self.version = version
        self.created_at = datetime.now(tz=timezone.utc)
        self.updated_at = datetime.now(tz=timezone.utc)
        self.submitted_at = submitted_at
        self.expires_at = expires_at


class EQSession:
    def __init__(
        self,
        eq_session_id: str,
        user_id: str | None,
        expires_at: datetime,
        session_data: str | None,
    ):
        self.eq_session_id = eq_session_id
        self.user_id = user_id
        self.session_data = session_data
        self.created_at = datetime.now(tz=timezone.utc)
        self.updated_at = datetime.now(tz=timezone.utc)
        self.expires_at = expires_at.replace(tzinfo=timezone.utc)


class UsedJtiClaim:
    def __init__(self, jti_claim: str, expires_at: datetime) -> None:
        self.jti_claim = jti_claim
        self.expires_at = expires_at.replace(tzinfo=timezone.utc)


# pylint: disable=no-self-use
class Timestamp(fields.Field):
    # pylint: disable=unused-argument
    def _serialize(
        self,
        value: datetime,
        *args: list | None,
        **kwargs: Any,
    ) -> int | None:
        if value:
            # Timezone aware datetime to timestamp
            return int(value.replace(tzinfo=timezone.utc).timestamp())

    # pylint: disable=unused-argument
    def _deserialize(
        self,
        value: float,
        *args: list | None,
        **kwargs: Any,
    ) -> datetime | None:
        if value:
            # Timestamp to timezone aware datetime
            return datetime.fromtimestamp(value, tz=timezone.utc)


class DateTimeSchemaMixin:
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    # pylint: disable=unused-argument
    @staticmethod
    @pre_dump
    def set_date(
        data: EQSession | QuestionnaireState,
        **kwargs: Any,
    ) -> EQSession | QuestionnaireState:
        data.updated_at = datetime.now(tz=timezone.utc)
        return data


class QuestionnaireStateSchema(Schema, DateTimeSchemaMixin):
    user_id = fields.Str()
    state_data = fields.Str()
    collection_exercise_sid = fields.Str()
    version = fields.Integer()
    submitted_at = Timestamp(allow_none=True)
    expires_at = Timestamp(allow_none=True)

    @post_load
    def make_model(
        self, data: dict, **kwargs: dict  # pylint: disable=unused-argument
    ) -> QuestionnaireState:
        created_at = data.pop("created_at", None)
        updated_at = data.pop("updated_at", None)
        model = QuestionnaireState(**data)
        model.created_at = created_at
        model.updated_at = updated_at
        return model


class EQSessionSchema(Schema, DateTimeSchemaMixin):
    eq_session_id = fields.Str()
    user_id = fields.Str()
    session_data = fields.Str()
    expires_at = Timestamp()

    @post_load
    def make_model(
        self, data: dict, **kwargs: dict  # pylint: disable=unused-argument
    ) -> EQSession:
        created_at = data.pop("created_at", None)
        updated_at = data.pop("updated_at", None)
        model = EQSession(**data)
        model.created_at = created_at
        model.updated_at = updated_at
        return model


class UsedJtiClaimSchema(Schema):
    jti_claim = fields.Str()
    expires_at = Timestamp()

    @post_load
    def make_model(
        self, data: dict, **kwargs: dict  # pylint: disable=unused-argument
    ) -> UsedJtiClaim:
        return UsedJtiClaim(**data)
