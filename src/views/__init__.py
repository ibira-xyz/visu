"""Init file for views module."""
from .index import render_index
from .post import render_post
from .not_found import render_not_found
from .server_error import render_server_error

__all__ = [
    "render_index",
    "render_post",
    "render_not_found",
    "render_server_error"
]
