import functools
from abc import ABC, abstractmethod
from datetime import datetime, timedelta, timezone
from typing import Callable, ParamSpec

from google.auth.credentials import Credentials
from google.auth.transport.requests import Request
from structlog import get_logger

from app.settings import OIDC_TOKEN_LEEWAY_IN_SECONDS, OIDC_TOKEN_VALIDITY_IN_SECONDS

P = ParamSpec("P")

logger = get_logger()
TTL = OIDC_TOKEN_VALIDITY_IN_SECONDS - OIDC_TOKEN_LEEWAY_IN_SECONDS


def get_expiry_from_ttl(ttl: int) -> datetime:
    return datetime.now(timezone.utc) - timedelta(seconds=ttl)


def is_naive(dt: datetime) -> bool:
    return dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None


def refresh_oidc_credentials(
    func: Callable[P, Credentials]
) -> Callable[P, Credentials]:
    """
    This decorator is used on implementations of the abstract method OIDCCredentialsService.get_credentials.
    This decorated method uses a ttl_cache decorator to discard fetched credentials after a given time.
    However, the TTL of the credentials should be determined by inspecting the expiry of the credentials
     themselves, not relying on the ttl_cache.
    As such, this decorator ensures the credentials returned from the ttl_cache are valid and refreshed
     via inspecting the expiry property of the credentials.
    Overall this ensures the caller is always returned valid credentials and credentials are cached to minimise
     API calls for credentials as well as discarded once invalid.
    """

    @functools.wraps(func)
    def wrapper_refresh_oidc_credentials(
        *args: P.args, **kwargs: P.kwargs
    ) -> Credentials:
        credentials = func(*args, **kwargs)
        expiry = credentials.expiry.replace(tzinfo=timezone.utc)
        if expiry < get_expiry_from_ttl(TTL):
            logger.info("refreshing oidc credentials", kwargs=kwargs)
            credentials.refresh(Request())
        return credentials

    return wrapper_refresh_oidc_credentials


class OIDCCredentialsService(ABC):
    @abstractmethod
    def get_credentials(
        self,
        *,
        iap_client_id: str,
    ) -> Credentials:
        pass
