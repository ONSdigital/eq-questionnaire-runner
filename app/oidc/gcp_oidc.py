from cachetools.func import ttl_cache
from google.auth.credentials import Credentials
from google.auth.transport.requests import Request
from google.oauth2.id_token import fetch_id_token_credentials
from structlog import get_logger

from app.oidc.oidc import TTL, OIDCCredentialsService, refresh_oidc_credentials

logger = get_logger()


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
