from cachetools.func import ttl_cache
from google.auth.credentials import AnonymousCredentials, Credentials
from google.auth.transport.requests import Request
from google.oauth2.id_token import fetch_id_token_credentials
from structlog import get_logger

from app.settings import OIDC_TOKEN_LEEWAY_IN_SECONDS

logger = get_logger()


class LocalOIDCCredentials:
    @staticmethod
    def get_credentials(
        iap_client_id: str,
    ) -> Credentials:
        logger.info("generating a local oidc token")
        logger.info(f"using IAP Client ID {iap_client_id}")

        # Return Credentials which do not provide any authentication or make any requests for tokens
        return AnonymousCredentials()


class OIDCCredentials:
    ttl = 3600 - OIDC_TOKEN_LEEWAY_IN_SECONDS

    @staticmethod
    @ttl_cache(maxsize=1, ttl=5)
    def get_credentials(
        *,
        iap_client_id: str,
    ) -> Credentials:
        logger.info("generating an oidc token")
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
