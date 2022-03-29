import pytest
from flask import url_for


@pytest.mark.usefixtures("app")
@pytest.mark.parametrize(
    "todo, expected",
    [
        (
            True,
            "/sign-out?todo=True",
        ),
        (
            False,
            "/sign-out?todo=False",
        ),
    ],
)
def test_url(todo, expected):
    url = url_for("session.get_sign_out", todo=todo)
    assert url == expected


@pytest.mark.usefixtures("app")
def test_url_no_args():
    url = url_for("session.get_sign_out")
    assert url == "/sign-out"
