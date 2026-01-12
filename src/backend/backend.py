"""Abstract base class for file readers."""
from abc import ABC, abstractmethod
from models import Post

class Backend(ABC):
    """Abstract base class for file readers."""
    
    @abstractmethod
    def get_post(self, slug: str) -> Post:
        """Get post description by slug."""

    @abstractmethod
    def get_content(self, content_uri: str) -> str:
        """Read content by its name or path."""

    @abstractmethod
    def get_all_posts(self) -> list[Post]:
        """Fetch data for the index view."""
