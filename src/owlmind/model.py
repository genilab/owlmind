from abc import ABC, abstractmethod

class Model(ABC):
    def __init__(self, host: str):
        self.host = host

    @abstractmethod
    def ping(self) -> bool:
        """Check if the provider is reachable."""
        pass

    @abstractmethod
    def info(self) -> list:
        """List available models."""
        pass

    @abstractmethod
    def query(self, model: str, prompt: str, **options):
        """Execute a completion request."""
        pass

