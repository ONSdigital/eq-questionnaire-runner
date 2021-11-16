from datetime import datetime, timezone

from marshmallow import Schema, fields, post_load, pre_dump


class QuestionnaireState:
    def __init__(
        self,
        user_id,
        state_data,
        collection_exercise_sid,
        version,
        submitted_at=None,
        expires_at=None,
    ):
        self.user_id = user_id
        self.state_data = state_data
        self.collection_exercise_sid = collection_exercise_sid
        self.version = version
        self.created_at = datetime.now(tz=timezone.utc)
        self.updated_at = datetime.now(tz=timezone.utc)
        self.submitted_at = submitted_at
        self.expires_at = expires_at.replace(tzinfo=timezone.utc)


class EQSession:
    def __init__(self, eq_session_id, user_id, expires_at, session_data):
        self.eq_session_id = eq_session_id
        self.user_id = user_id
        self.session_data = session_data
        self.created_at = datetime.now(tz=timezone.utc)
        self.updated_at = datetime.now(tz=timezone.utc)
        self.expires_at = expires_at.replace(tzinfo=timezone.utc)


class UsedJtiClaim:
    def __init__(self, jti_claim, expires_at):
        self.jti_claim = jti_claim
        self.expires_at = expires_at.replace(tzinfo=timezone.utc)


# pylint: disable=no-self-use
class Timestamp(fields.Field):
    def _serialize(self, value, *args, **kwargs):  # pylint: disable=unused-argument
        if value:
            # Timezone aware datetime to timestamp
            return int(value.replace(tzinfo=timezone.utc).timestamp())

    def _deserialize(self, value, *args, **kwargs):  # pylint: disable=unused-argument
        if value:
            # Timestamp to timezone aware datetime
            return datetime.fromtimestamp(value, tz=timezone.utc)


class DateTimeSchemaMixin:
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    @pre_dump
    def set_date(self, data, **kwargs):  # pylint: disable=unused-argument
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
    def make_model(self, data, **kwargs):  # pylint: disable=unused-argument
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
    def make_model(self, data, **kwargs):  # pylint: disable=unused-argument
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
    def make_model(self, data, **kwargs):  # pylint: disable=unused-argument
        return UsedJtiClaim(**data)
