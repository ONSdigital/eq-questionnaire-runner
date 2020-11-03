from abc import ABC, abstractmethod


class FulfilmentRequest(ABC):
    @property
    @abstractmethod
    def payload(self) -> bytes:
        pass  # pragma: no cover
