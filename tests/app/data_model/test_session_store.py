from datetime import datetime, timezone

import pytest
from flask import current_app
from jwcrypto import jwe
from jwcrypto.common import base64url_encode

from app.data_models import SessionData
from app.data_models.app_models import EQSession
from app.data_models.session_store import SessionStore
from app.utilities.json import json_dumps


def test_no_session(app, app_session_store):
    with app.test_request_context():
        assert app_session_store.session_store.user_id is None
        assert app_session_store.session_store.session_data is None


def test_create(app, app_session_store):
    with app.test_request_context():
        app_session_store.session_store.create(
            "eq_session_id",
            "test",
            app_session_store.session_data,
            app_session_store.expires_at,
        )
        assert "eq_session_id" == app_session_store.session_store.eq_session_id
        assert "test" == app_session_store.session_store.user_id
        assert (
            app_session_store.session_data
            == app_session_store.session_store.session_data
        )


def test_save(app, app_session_store):
    with app.test_request_context():
        app_session_store.session_store.create(
            eq_session_id="eq_session_id",
            user_id="test",
            session_data=app_session_store.session_data,
            expires_at=app_session_store.expires_at,
        ).save()
        session_store = SessionStore("user_ik", "pepper", "eq_session_id")

        assert session_store.session_data.confirmation_email_count == 0


def test_delete(app, app_session_store):
    with app.test_request_context():
        app_session_store.session_store.create(
            eq_session_id="eq_session_id",
            user_id="test",
            session_data=app_session_store.session_data,
            expires_at=app_session_store.expires_at,
        ).save()
        assert "test" == app_session_store.session_store.user_id
        app_session_store.session_store.delete()
        assert app_session_store.session_store.user_id is None


def test_add_data_to_session(app, app_session_store):
    with app.test_request_context():
        app_session_store.session_store.create(
            eq_session_id="eq_session_id",
            user_id="test",
            session_data=app_session_store.session_data,
            expires_at=app_session_store.expires_at,
        ).save()
        feedback_count = 9
        app_session_store.session_store.session_data.feedback_count = feedback_count
        app_session_store.session_store.save()

        session_store = SessionStore("user_ik", "pepper", "eq_session_id")
        assert session_store.session_data.feedback_count == 9


def test_should_not_delete_when_no_session(app, app_session_store):
    with app.test_request_context("/status") as context:
        # Call clear with a valid user_id but no session in database
        app_session_store.session_store.delete()

        # No database calls should have been made
        assert context.app.eq["storage"].client.delete_call_count == 0


def test_session_store_ignores_new_values_in_session_data(
    app, app_session_store, session_data
):
    session_data.additional_value = "some cool new value you do not know about yet"

    with app.test_request_context():
        app_session_store.session_store.create(
            eq_session_id="eq_session_id",
            user_id="test",
            session_data=app_session_store.session_data,
            expires_at=app_session_store.expires_at,
        ).save()

        session_store = SessionStore("user_ik", "pepper", "eq_session_id")

        assert hasattr(session_store.session_data, "additional_value") is False


def test_session_store_ignores_multiple_new_values_in_session_data(
    app, app_session_store, session_data
):
    session_data.additional_value = "some cool new value you do not know about yet"
    session_data.second_additional_value = "some other not so cool value"

    with app.test_request_context():
        app_session_store.session_store.create(
            eq_session_id="eq_session_id",
            user_id="test",
            session_data=session_data,
            expires_at=app_session_store.expires_at,
        ).save()

        session_store = SessionStore("user_ik", "pepper", "eq_session_id")

        assert hasattr(session_store.session_data, "additional_value") is False
        assert hasattr(session_store.session_data, "second_additional_value") is False


def test_session_store_stores_trading_as_value_if_present(
    app, app_session_store, session_data
):
    with app.test_request_context():
        app_session_store.session_store.create(
            eq_session_id="eq_session_id",
            user_id="test",
            session_data=session_data,
            expires_at=app_session_store.expires_at,
        ).save()

        session_store = SessionStore("user_ik", "pepper", "eq_session_id")

        assert hasattr(session_store.session_data, "trad_as") is True


def test_session_store_stores_none_for_trading_as_if_not_present(
    app, app_session_store, session_data
):
    session_data.trad_as = None
    with app.test_request_context():
        app_session_store.session_store.create(
            eq_session_id="eq_session_id",
            user_id="test",
            session_data=session_data,
            expires_at=app_session_store.expires_at,
        ).save()

        session_store = SessionStore("user_ik", "pepper", "eq_session_id")

        assert session_store.session_data.trad_as is None


def test_load_existing_session_does_not_error_when_session_data_contains_survey_url(
    app, app_session_store
):
    session_data_with_survey_url = SessionData(
        tx_id="123",
        schema_name="some_schema_name",
        display_address="68 Abingdon Road, Goathill",
        period_str=None,
        language_code="cy",
        launch_language_code="en",
        survey_url="some-url",
        ru_name=None,
        ru_ref=None,
        submitted_at=datetime.now(timezone.utc).isoformat(),
        response_id="321",
        case_id="789",
    )

    with app.test_request_context():
        # Given a session store with session data that has a survey url
        app_session_store.session_store.create(
            eq_session_id="eq_session_id",
            user_id="test",
            session_data=session_data_with_survey_url,
            expires_at=app_session_store.expires_at,
        ).save()

        # When a SessionStore is loaded (Session matching 'eq_session_id' exists at this point)
        loaded_session_store = SessionStore("user_ik", "pepper", "eq_session_id")

        # Then
        assert (
            loaded_session_store.session_data.__dict__
            == session_data_with_survey_url.__dict__
        )
        assert loaded_session_store.session_data.survey_url is None


@pytest.mark.usefixtures("app")
def test_legacy_load(app_session_store_encoded):
    _save_session(
        app_session_store_encoded,
        app_session_store_encoded.session_id,
        app_session_store_encoded.user_id,
        app_session_store_encoded.session_data,
        legacy=True,
    )
    session_store = SessionStore(
        app_session_store_encoded.user_ik,
        app_session_store_encoded.pepper,
        app_session_store_encoded.session_id,
    )

    assert (
        session_store.session_data.tx_id == app_session_store_encoded.session_data.tx_id
    )


@pytest.mark.usefixtures("app")
def test_load(app_session_store_encoded):
    _save_session(
        app_session_store_encoded,
        app_session_store_encoded.session_id,
        app_session_store_encoded.user_id,
        app_session_store_encoded.session_data,
    )
    session_store = SessionStore(
        app_session_store_encoded.user_ik,
        app_session_store_encoded.pepper,
        app_session_store_encoded.session_id,
    )
    assert (
        session_store.session_data.tx_id == app_session_store_encoded.session_data.tx_id
    )


def _save_session(app_session, session_id, user_id, data, legacy=False):
    raw_data = json_dumps(vars(data))
    protected_header = {"alg": "dir", "enc": "A256GCM", "kid": "1,1"}

    if legacy:
        plaintext = base64url_encode(raw_data)
    else:
        plaintext = raw_data

    jwe_token = jwe.JWE(
        plaintext=plaintext, protected=protected_header, recipient=app_session.key
    )

    session_model = EQSession(
        eq_session_id=session_id,
        user_id=user_id,
        session_data=jwe_token.serialize(compact=True),
        expires_at=app_session.expires_at,
    )
    current_app.eq["storage"].put(session_model)
