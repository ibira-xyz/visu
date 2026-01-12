"""Controller for processing post content into Post entities."""

import re

from backend.backend import Backend
from models import Post, PostContent
from parsers import parse_markdown, process_date, ContentElementParser


def create_post_content(slug: str,
                        content: str,
                        content_elements: list,
                        backend: Backend) -> PostContent:
    """Process content items and return combined HTML with placeholder substitution."""
    markdown_content = backend.get_content(content)
    html = parse_markdown(markdown_content)

    processor = ContentElementParser(content_elements)

    processed_html = re.sub(processor.placeholder_pattern, processor.replace_placeholder, html)

    return PostContent(
        slug=slug,
        article=processed_html,
        component_scripts=processor.component_scripts
    )

def process_post(post: Post, backend: Backend) -> dict:
    """Process raw post content into a Post entity."""
    return {'post': post,
            'post_content': create_post_content(post.slug,
                                                post.content,
                                                post.content_elements,
                                                backend),
            'formatted_date': process_date(post.date)}
