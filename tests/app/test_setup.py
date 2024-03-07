import pytest
from mock import MagicMock

from app.helpers import get_span_and_trace
from app.setup import setup_secure_cookies


@pytest.mark.parametrize(
    "cloud_trace_header, expected_trace, expected_span",
    (
        (
            {"X-Cloud-Trace-Context": "0123456789/0123456789012345678901;o=1"},
            "0123456789",
            "0123456789012345678901",
        ),
        ({}, None, None),
        ({"X-Cloud-Trace-Context": "not a real trace context"}, None, None),
        ({"X-Cloud-Trace-Context": ""}, None, None),
        ({"X-Cloud-Trace-Context": None}, None, None),
        (
            {"not a real trace context": "0123456789/0123456789012345678901;o=1"},
            None,
            None,
        ),
    ),
)
def test_get_span_and_trace(cloud_trace_header, expected_trace, expected_span):
    span, trace = get_span_and_trace(cloud_trace_header)
    assert trace == expected_trace
    assert span == expected_span


def test_setup_secure_cookies_missing_secret_key():
    app = MagicMock()
    app.eq = {"secret_store": MagicMock()}
    app.secret_key = None

    app.eq["secret_store"].get_secret_by_name.return_value = None

    with pytest.raises(ValueError):
        setup_secure_cookies(app)

    assert app.secret_key is None
