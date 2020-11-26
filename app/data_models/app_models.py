from datetime import datetime

from dateutil.tz import tzutc
from marshmallow import Schema, fields, post_load, pre_dump


class QuestionnaireState:
    def __init__(self, user_id, state_data, version):
        self.user_id = user_id
        self.state_data = state_data
        self.version = version
        self.created_at = datetime.now(tz=tzutc())
        self.updated_at = datetime.now(tz=tzutc())


class EQSession:
    def __init__(self, eq_session_id, user_id, expires_at, session_data=None):
        self.eq_session_id = eq_session_id
        self.user_id = user_id
        self.session_data = session_data
        self.created_at = datetime.now(tz=tzutc())
        self.updated_at = datetime.now(tz=tzutc())
        self.expires_at = expires_at.replace(tzinfo=tzutc())


class UsedJtiClaim:
    def __init__(self, jti_claim, expires_at):
        self.jti_claim = jti_claim
        self.expires_at = expires_at.replace(tzinfo=tzutc())


# pylint: disable=no-self-use
class Timestamp(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value:
            # Timezone aware datetime to timestamp
            return int(value.replace(tzinfo=tzutc()).strftime("%s"))

    def _deserialize(self, value, attr, data, **kwargs):
        if value:
            # Timestamp to timezone aware datetime
            return datetime.utcfromtimestamp(value).replace(tzinfo=tzutc())


class DateTimeSchemaMixin:
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    @pre_dump
    def set_date(self, data, **kwargs):
        data.updated_at = datetime.now(tz=tzutc())
        return data


class QuestionnaireStateSchema(Schema, DateTimeSchemaMixin):
    user_id = fields.Str()
    state_data = fields.Str()
    version = fields.Integer()

    @post_load
    def make_model(self, data, **kwargs):
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
    def make_model(self, data, **kwargs):
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
    def make_model(self, data, **kwargs):
        return UsedJtiClaim(**data)
