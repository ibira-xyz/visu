"""Controller for processing post content into Post entities."""

from bs4 import BeautifulSoup

from config.app_config import AppConfig
from models import Post
from parsers import parse_markdown, process_date

config = AppConfig()

class PostController:
    """Processes post content with mixed markdown and image elements."""

    def __init__(self, backend):
        self.backend = backend
        self.cdn_url = config.get('static_url')

    def _process_content(self, content_items):
        """Process content items and return combined HTML."""
        soup = BeautifulSoup("", "html.parser")

        for item in content_items:
            item_type = item.get('type')

            if item_type == 'markdown':
                markdown_content = self.backend.get_content(item['path'])
                html = parse_markdown(markdown_content)
                soup.append(BeautifulSoup(html, "html.parser"))

            elif item_type == 'image':
                figure = soup.new_tag('figure', **{'class': 'post-image-figure'})

                img = soup.new_tag('img',
                                  src=f'{self.cdn_url}{item["path"]}',
                                  alt=item.get('description', ''),
                                  **{'class': 'post-image'})
                figure.append(img)

                if item.get('legend'):
                    figcaption = soup.new_tag('figcaption', **{'class': 'post-image-caption'})
                    figcaption.string = item['legend']
                    figure.append(figcaption)

                soup.append(figure)

        return str(soup)

    def run(self, post: Post) -> Post:
        """Process raw post content into a Post entity."""
        processed_content = self._process_content(post.content_metadata)
        return {'post': post,
                'post_content': processed_content,
                'formatted_date': process_date(post.date)}
