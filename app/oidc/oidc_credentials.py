import functools
from abc import ABC, abstractmethod
from datetime import datetime, timedelta, timezone

from cachetools.func import ttl_cache
from google.auth.credentials import AnonymousCredentials, Credentials
from google.auth.transport.requests import Request
from google.oauth2.id_token import fetch_id_token_credentials
from structlog import get_logger

from app.settings import OIDC_TOKEN_LEEWAY_IN_SECONDS

logger = get_logger()
TTL = 3600 - OIDC_TOKEN_LEEWAY_IN_SECONDS  # 1 hour minus leeway in seconds


def refresh_oidc_credentials(func):
    """
    This decorator is used on the method OIDCCredentialsService.get_credentials.
    This decorated method uses a ttl_cache decorator to discard fetched credentials after a given time.
    However, the TTL of the credentials should be determined by inspecting the expiry of the credentials
     themselves, not relying on the ttl_cache.
    As such, this decorator ensures the credentials returned from the ttl_cache are valid and refreshed
     via inspecting the expiry property of the credentials.
    Overall this ensures the caller is always returned valid credentials and credentials are cached to minimise
     API calls for credentials as well as discarded once invalid.
    """

    @functools.wraps(func)
    def wrapper_refresh_oidc_credentials(*args, **kwargs):
        credentials = func(*args, **kwargs)
        if credentials.expiry < datetime.now(timezone.utc) - timedelta(seconds=TTL):
            logger.info("refreshing oidc credentials")
            credentials.refresh(Request())
        return credentials

    return wrapper_refresh_oidc_credentials


class LocalOIDCCredentials(AnonymousCredentials):
    def refresh(self, request):
        pass


class OIDCCredentialsService(ABC):
    @abstractmethod
    def get_credentials(
            self,
            *,
            iap_client_id: str,
    ):
        pass


class LocalOIDCCredentialsService(OIDCCredentialsService):
    @refresh_oidc_credentials
    @ttl_cache(maxsize=None, ttl=TTL)
    def get_credentials(
            self,
            *,
            iap_client_id: str,
    ) -> Credentials:
        logger.info("generating local oidc credentials")
        logger.info(f"using IAP Client ID {iap_client_id}")

        # Return Credentials which do not provide any authentication or make any requests for tokens
        return LocalOIDCCredentials()


class GCPCredentialsService(OIDCCredentialsService):
    @refresh_oidc_credentials
    @ttl_cache(maxsize=None, ttl=TTL)
    def get_credentials(
            self,
            *,
            iap_client_id: str,
    ) -> Credentials:
        logger.info("fetching oidc credentials from GCP")
        logger.info(f"using IAP Client ID {iap_client_id}")

        request = Request()
        target_audience = iap_client_id

        # Create ID token credentials.
        credentials = fetch_id_token_credentials(
            audience=target_audience, request=request
        )

        # Refresh the credential to obtain an ID token.
        credentials.refresh(request)

        # Return the generated credentials
        return credentials
