"""Controller for processing post content into Post entities."""

from bs4 import BeautifulSoup

from backend.backend import Backend
from config.app_config import AppConfig
from models import Post
from parsers import parse_markdown, process_date

config = AppConfig()


def _process_content(content_items: list, backend: Backend) -> str:
    """Process content items and return combined HTML."""
    soup = BeautifulSoup("", "html.parser")
    cdn_url = config.get('static_url')

    for item in content_items:
        item_type = item.get('type')

        if item_type == 'markdown':
            markdown_content = backend.get_content(item['path'])
            html = parse_markdown(markdown_content)
            soup.append(BeautifulSoup(html, "html.parser"))

        elif item_type == 'image':
            figure = soup.new_tag('figure', **{'class': 'post-image-figure'})

            img = soup.new_tag('img',
                                src=f'{cdn_url}{item["path"]}',
                                alt=item.get('description', ''),
                                **{'class': 'post-image'})
            figure.append(img)

            if item.get('legend'):
                figcaption = soup.new_tag('figcaption', **{'class': 'post-image-caption'})
                figcaption.string = item['legend']
                figure.append(figcaption)

            soup.append(figure)

    return str(soup)

def process_post(post: Post, backend: Backend) -> dict:
    """Process raw post content into a Post entity."""
    return {'post': post,
            'post_content': _process_content(post.content_metadata, backend),
            'formatted_date': process_date(post.date)}
