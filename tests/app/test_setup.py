import pytest
from unittest.mock import MagicMock
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

def test_setup_secure_cookies_with_missing_secret_key():
   # Create a mock Flask application
    app = MagicMock()
    app.eq = {"secret_store": MagicMock()}
    app.secret_key = None
    
    # Mocking the get_secret_by_name method to return None
    app.eq["secret_store"].get_secret_by_name.return_value = None

    # Test setup_secure_cookies
    with pytest.raises(ValueError):
        setup_secure_cookies(app)
    
    # Assert that the secret_key and session_interface remain None
    assert app.secret_key is None