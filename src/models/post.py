"""Module defining the Post entity."""
from collections import namedtuple

Post = namedtuple('Post', [
    'title',
    'content_metadata',
    'description',
    'date',
    'author',
    'banner',
    'slug',
    'tags'
])
