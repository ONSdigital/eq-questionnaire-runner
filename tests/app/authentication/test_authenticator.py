from datetime import datetime, timezone

from flask import Flask
from flask import session as cookie_session
from flask.wrappers import Request
from mock import Mock

from app.authentication.authenticator import load_user, request_load_user, user_loader
from app.data_models.metadata_proxy import MetadataProxy
from app.settings import USER_IK


def test_check_session_with_user_id_in_session(
    app,
    session_store,
    session_data,
    expires_at,
    mocker,
):
    mocker.patch(
        "app.authentication.authenticator.get_session_store", return_value=session_store
    )
    with app.app_context():
        # Given
        session_store.create("eq_session_id", "user_id", session_data, expires_at)
        cookie_session[USER_IK] = "user_ik"

        # When
        user = load_user()

        # Then
        assert user.user_id == "user_id"
        assert user.user_ik == "user_ik"


def test_check_session_with_no_user_id_in_session(app, mocker):
    mocker.patch(
        "app.authentication.authenticator.get_session_store", return_value=None
    )

    with app.app_context():
        # Given / When
        user = load_user()

        # Then
        assert user is None


def test_load_user(
    app,
    session_store,
    session_data,
    expires_at,
    mocker,
):
    mocker.patch(
        "app.authentication.authenticator.get_session_store", return_value=session_store
    )
    with app.app_context():
        # Given
        session_store.create(
            "eq_session_id",
            "user_id",
            session_data,
            expires_at,
        )
        cookie_session[USER_IK] = "user_ik"

        # When
        user = user_loader(None)

        # Then
        assert user.user_id == "user_id"
        assert user.user_ik == "user_ik"


def test_request_load_user(
    app,
    session_store,
    session_data,
    expires_at,
    mocker,
):
    mocker.patch(
        "app.authentication.authenticator.get_session_store",
        return_value=session_store,
    )
    with app.app_context():
        # Given
        session_store.create("eq_session_id", "user_id", session_data, expires_at)
        cookie_session[USER_IK] = "user_ik"

        # When
        user = request_load_user(mocker.Mock(Request))

        # Then
        assert user.user_id == "user_id"
        assert user.user_ik == "user_ik"


def test_no_user_when_session_has_expired(
    app,
    session_store,
    session_data,
    mocker,
):
    mocker.patch(
        "app.authentication.authenticator.get_session_store", return_value=session_store
    )
    with app.app_context():
        # Given
        session_store.create(
            "eq_session_id",
            "user_id",
            session_data,
            expires_at=datetime.now(timezone.utc),
        )
        cookie_session[USER_IK] = "user_ik"

        # When
        user = user_loader(None)

        # Then
        assert user is None
        assert cookie_session.get(USER_IK) is None


def test_valid_user_does_not_extend_session_expiry_when_expiry_less_than_60_seconds_different(
    app: Flask,
    session_store,
    session_data,
    expires_at,
    mocker,
):
    mocker.patch(
        "app.authentication.authenticator.get_session_store", return_value=session_store
    )
    with app.app_context():
        # Given
        session_store.create("eq_session_id", "user_id", session_data, expires_at)
        cookie_session[USER_IK] = "user_ik"
        cookie_session["expires_in"] = 5

        # When
        user = user_loader(None)

        # Then
        assert user.user_id == "user_id"
        assert user.user_ik == "user_ik"
        assert user.is_authenticated is True
        assert session_store.expiration_time == expires_at


def test_valid_user_extends_session_expiry_when_expiry_greater_than_60_seconds_different(
    app,
    session_store,
    session_data,
    expires_at,
    mocker,
):
    mocker.patch(
        "app.authentication.authenticator.get_session_store", return_value=session_store
    )
    with app.app_context():
        # Given
        session_store.create("eq_session_id", "user_id", session_data, expires_at)
        cookie_session[USER_IK] = "user_ik"
        cookie_session["expires_in"] = 600

        # When
        user = user_loader(None)

        # Then
        assert user.user_id == "user_id"
        assert user.user_ik == "user_ik"
        assert user.is_authenticated is True
        assert session_store.expiration_time > expires_at
