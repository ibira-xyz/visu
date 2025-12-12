"""Init file for renderers module."""
from .index import render_index
from .post import render_post

__all__ = ["render_index", "render_post"]
