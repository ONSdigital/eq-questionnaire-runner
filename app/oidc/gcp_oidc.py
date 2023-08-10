from cachetools.func import ttl_cache
from google.auth.credentials import Credentials
from google.auth.transport.requests import Request
from google.oauth2.id_token import fetch_id_token_credentials
from structlog import get_logger

from app.oidc.oidc import OIDCCredentialsService
from app.settings import OIDC_TOKEN_LEEWAY_IN_SECONDS, OIDC_TOKEN_VALIDITY_IN_SECONDS

TTL = OIDC_TOKEN_VALIDITY_IN_SECONDS - OIDC_TOKEN_LEEWAY_IN_SECONDS

logger = get_logger()


class OIDCCredentialsServiceGCP(OIDCCredentialsService):
    @staticmethod
    @ttl_cache(maxsize=None, ttl=TTL)
    def get_credentials(*, iap_client_id: str) -> Credentials:
        """
        The credentials are valid for OIDC_TOKEN_VALIDITY_IN_SECONDS, and we use a ttl cache of this minus a configurable leeway
        this is to ensure that even in the edge case where the timers on the cache and the credentials don't quite align,
        the OIDC_TOKEN_LEEWAY_IN_SECONDS should be more than enough to cover it and guarantee safety
        """
        logger.info("fetching OIDC credentials from GCP", iap_client_id=iap_client_id)

        request = Request()

        credentials = fetch_id_token_credentials(
            audience=iap_client_id, request=request
        )

        # Refresh the credential to obtain an ID token.
        credentials.refresh(request)

        return credentials
