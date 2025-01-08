from datetime import datetime

import pytest

from app import settings


@pytest.mark.parametrize(
    "value, minimum, expected",
    (
        (1, 1000, 1000),
        (1000, 10000, 10000),
    ),
)
def test_ensure_min_returns(value, minimum, expected):
    assert settings.ensure_min(value, minimum) == expected


@pytest.mark.parametrize(
    "file, expected",
    (
        (".application-version", True),
        (".missing-application-version", False),
        (None, False),
        ("", False),
    ),
)
def test_read_files(file, expected):
    assert bool(settings.read_file(file)) is expected


def test_invalid_key_raises_exception():
    with pytest.raises(Exception) as exception:
        settings.get_env_or_fail("MISSING_ENVIRONMENT_VARIABLE")

        assert "Setting 'MISSING_ENVIRONMENT_VARIABLE' Missing" == str(
            exception.exception
        )
