import pytest

from app.helpers import get_span_and_trace


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
