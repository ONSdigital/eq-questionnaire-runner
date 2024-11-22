from werkzeug.datastructures import EnvironHeaders


def get_span_and_trace(
    headers: EnvironHeaders,
) -> tuple[None, None] | tuple[str, str]:
    try:
        trace, span = headers.get("X-Cloud-Trace-Context").split("/")  # type: ignore
    except (ValueError, AttributeError):
        return None, None

    span = span.split(";")[0]
    return span, trace
