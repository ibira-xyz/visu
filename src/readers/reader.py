"""Abstract base class for file readers."""
from abc import ABC, abstractmethod

class Reader(ABC):
    """Abstract base class for file readers."""

    @abstractmethod
    def read(self):
        """Read the content from the source."""
