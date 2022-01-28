from datetime import datetime, timezone

from app.data_models.app_models import EQSession, QuestionnaireState, UsedJtiClaim
from app.storage.storage import StorageModel

NOW = datetime.now(tz=timezone.utc).replace(microsecond=0)


def create_model(model):
    config = StorageModel.TABLE_CONFIG_BY_TYPE[type(model)]
    schema = config["schema"]()

    item = schema.dump(model)
    new_model = schema.load(item)

    return new_model


def test_used_jti_claim():
    model = UsedJtiClaim("claimid", NOW)

    assert create_model(model).__dict__ == model.__dict__


def test_eq_session():
    model = EQSession(
        eq_session_id="sessionid",
        user_id="someuser",
        session_data="somedata",
        expires_at=NOW,
    )
    new_model = create_model(model)

    assert new_model.__dict__ == model.__dict__
    assert new_model.created_at >= NOW
    assert new_model.updated_at >= NOW
    assert new_model.expires_at >= NOW


def test_questionnaire_state():
    model = QuestionnaireState("someuser", "somedata", "ce_sid", 1)
    new_model = create_model(model)

    assert new_model.__dict__ == model.__dict__
    assert new_model.created_at >= NOW
    assert new_model.updated_at >= NOW
