"""Module defining the Post entity."""
from typing import NamedTuple

class PostContent(NamedTuple):
    """Data structure representing a blog post."""
    slug: str
    article: str
    component_scripts: list[str]
