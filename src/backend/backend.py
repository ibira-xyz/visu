"""Abstract base class for file readers."""
from abc import ABC, abstractmethod

class Backend(ABC):
    """Abstract base class for file readers."""

    @abstractmethod
    def get_post(self, slug):
        """Get post description by slug."""

    @abstractmethod
    def get_content(self, content_uri):
        """Read content by its name or path."""
