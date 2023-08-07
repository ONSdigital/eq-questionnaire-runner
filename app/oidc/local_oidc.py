from functools import lru_cache

from google.auth.credentials import AnonymousCredentials, Credentials
from structlog import get_logger

from app.oidc.oidc import OIDCCredentialsService

logger = get_logger()


class OIDCCredentialsServiceLocal(OIDCCredentialsService):
    @staticmethod
    @lru_cache
    def get_credentials(*, iap_client_id: str) -> Credentials:
        """
        Anonymous credentials don't expire so can be generated once and cached
        """
        logger.info("generating local oidc credential", iap_client_id=iap_client_id)

        # Return Credentials which do not provide any authentication or make any requests for tokens
        return AnonymousCredentials()
