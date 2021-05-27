from app.settings import CENSUS_CY_BASE_URL, CENSUS_EN_BASE_URL, CENSUS_NIR_BASE_URL

from .address_lookup_api_helper import get_address_lookup_api_auth_token
from .header_helpers import get_span_and_trace
from .url_safe_serializer import url_safe_serializer


def get_base_url(schema_theme: str, language_code: str) -> str:
    if language_code == "cy":
        return CENSUS_CY_BASE_URL

    if schema_theme == "census-nisra":
        return CENSUS_NIR_BASE_URL

    return CENSUS_EN_BASE_URL


__all__ = [
    "get_base_url",
    "get_span_and_trace",
    "url_safe_serializer",
    "get_address_lookup_api_auth_token",
]
