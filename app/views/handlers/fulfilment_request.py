from abc import ABC, abstractmethod


class FulfilmentRequest(ABC):
    @property
    @abstractmethod
    def payload(self) -> bytes:
        pass  # pragma: no cover


class FulfilmentRequestPublicationFailed(Exception):
    def __init__(self, message="", invoked_by=None):
        super().__init__(message)
        self.invoked_by = invoked_by
