from abc import ABC, abstractmethod

from google.auth.credentials import Credentials


class OIDCCredentialsService(ABC):
    @staticmethod
    @abstractmethod
    def get_credentials(*, iap_client_id: str) -> Credentials:  # pragma no cover
        ...
