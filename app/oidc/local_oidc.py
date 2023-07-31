from cachetools.func import ttl_cache
from google.auth.credentials import AnonymousCredentials, Credentials
from google.auth.transport import Request
from structlog import get_logger

from app.oidc.oidc import (
    TTL,
    OIDCCredentialsService,
    get_expiry_from_ttl,
    refresh_oidc_credentials,
)

logger = get_logger()


class LocalOIDCCredentials(AnonymousCredentials):
    # Type ignore: AnonymousCredentials has no constructor and does not call its parent's constructor
    def __init__(self) -> None:  # pylint: disable=super-init-not-called
        self.expiry = get_expiry_from_ttl(TTL)

    def refresh(self, request: Request) -> None:
        pass


class OIDCCredentialsServiceLocal(OIDCCredentialsService):
    @refresh_oidc_credentials
    @ttl_cache(maxsize=None, ttl=TTL)
    def get_credentials(
        self,
        *,
        iap_client_id: str,
    ) -> Credentials:
        logger.info("generating local oidc credential", iap_client_id=iap_client_id)

        # Return Credentials which do not provide any authentication or make any requests for tokens
        return LocalOIDCCredentials()
