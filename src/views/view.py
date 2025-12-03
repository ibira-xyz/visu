"""Abstract base class for views."""
from abc import ABC, abstractmethod
from collections import namedtuple

from jinja2 import Environment, FileSystemLoader


class View(ABC):
    """Abstract base class for all views."""
    def __init__(self, searchpath: str):
        self.template_env = Environment(loader=FileSystemLoader(searchpath))

    @abstractmethod
    def render(self, context: namedtuple) -> str:
        """Render the view with the given context."""
