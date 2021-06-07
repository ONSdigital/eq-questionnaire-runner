from .address_lookup_api_helper import get_address_lookup_api_auth_token
from .header_helpers import get_span_and_trace
from .template_helpers import context_options
from .url_safe_serializer import url_safe_serializer


def get_base_url(schema_theme: str, language_code: str) -> str:
    return context_options(schema_theme, language_code).base_url


__all__ = [
    "get_base_url",
    "get_span_and_trace",
    "url_safe_serializer",
    "get_address_lookup_api_auth_token",
]
