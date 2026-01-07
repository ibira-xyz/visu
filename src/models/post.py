"""Module defining the Post entity."""
from typing import NamedTuple

class Post(NamedTuple):
    """Data structure representing a blog post."""
    title: str
    content: str
    content_elements: list[dict]
    description: str
    date: str
    author: str
    banner: str
    slug: str
    tags: list[str]
