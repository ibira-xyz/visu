"""Base Style Module"""
from abc import ABC, abstractmethod

class BaseStyle(ABC):
    """Abstract base class for styles."""
    @abstractmethod
    def get_tags(self):
        """Return a list of tags relevant to the style."""

    @abstractmethod
    def get_class(self, tag):
        """Return the class name for a given tag."""
