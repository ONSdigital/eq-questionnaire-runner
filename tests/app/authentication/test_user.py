import pytest

from app.authentication.user import User


def test_get_user_id():
    user = User("1", "2")
    assert "1" == user.user_id


def test_get_user_ik():
    user = User("1", "2")
    assert "2" == user.user_ik


def test_negative_user():
    user = User("-1", "2")
    assert "-1" == user.user_id


def test_no_user():
    with pytest.raises(ValueError):
        User("", "")


def test_none_user():
    with pytest.raises(ValueError):
        User(None, "2")
