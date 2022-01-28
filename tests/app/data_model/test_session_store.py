import pytest
from flask import current_app
from jwcrypto import jwe
from jwcrypto.common import base64url_encode

from app.data_models.app_models import EQSession
from app.data_models.session_data import SessionData
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
        assert session_store.session_data.tx_id == "tx_id"


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
        display_address = "68 Abingdon Road, Goathill"
        app_session_store.session_store.session_data.display_address = display_address
        app_session_store.session_store.save()

        session_store = SessionStore("user_ik", "pepper", "eq_session_id")
        assert session_store.session_data.display_address == display_address


def test_should_not_delete_when_no_session(app, app_session_store):
    with app.test_request_context("/status") as context:
        # Call clear with a valid user_id but no session in database
        app_session_store.session_store.delete()

        # No database calls should have been made
        assert context.app.eq["storage"].client.delete_call_count == 0


def test_session_store_ignores_new_values_in_session_data(app, app_session_store):
    session_data = SessionData(
        tx_id="tx_id",
        schema_name="some_schema_name",
        period_str="period_str",
        language_code=None,
        launch_language_code=None,
        survey_url=None,
        ru_name="ru_name",
        ru_ref="ru_ref",
        response_id="response_id",
        case_id="case_id",
    )

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
    app, app_session_store
):
    session_data = SessionData(
        tx_id="tx_id",
        schema_name="some_schema_name",
        period_str="period_str",
        language_code=None,
        launch_language_code=None,
        survey_url=None,
        ru_name="ru_name",
        ru_ref="ru_ref",
        response_id="response_id",
        case_id="case_id",
    )

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


def test_session_store_stores_trading_as_value_if_present(app, app_session_store):
    session_data = SessionData(
        tx_id="tx_id",
        schema_name="some_schema_name",
        period_str="period_str",
        language_code=None,
        launch_language_code=None,
        survey_url=None,
        ru_name="ru_name",
        ru_ref="ru_ref",
        response_id="response_id",
        trad_as="trading_as",
        case_id="case_id",
    )
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
    app, app_session_store
):
    session_data = SessionData(
        tx_id="tx_id",
        schema_name="some_schema_name",
        period_str="period_str",
        language_code=None,
        launch_language_code=None,
        survey_url=None,
        ru_name="ru_name",
        ru_ref="ru_ref",
        response_id="response_id",
        case_id="case_id",
    )
    with app.test_request_context():
        app_session_store.session_store.create(
            eq_session_id="eq_session_id",
            user_id="test",
            session_data=session_data,
            expires_at=app_session_store.expires_at,
        ).save()

        session_store = SessionStore("user_ik", "pepper", "eq_session_id")

        assert session_store.session_data.trad_as is None


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
