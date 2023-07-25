from uuid import uuid4

from structlog import get_logger

logger = get_logger()


class LogOIDCTokenGenerator:
    @staticmethod
    def generate_token(
        iap_client_id: str,
    ) -> str:
        logger.info("generating an oidc token")
        logger.info(f"using mocked IAP Client ID {iap_client_id}")

        return str(uuid4())


class OIDCTokenGenerator:
    def __init__(self) -> None:
        return

    def generate_token(
        self,
        iap_client_id: str,
    ) -> str:
        logger.info("generating an oidc token")
        logger.info(f"using IAP Client ID {iap_client_id}")

        return str(uuid4())
