"""Controller for processing post content into Post entities."""

import datetime
from bs4 import BeautifulSoup

from models.post import Post
from parsers import parse_markdown


dict_mes = {
    1: "janeiro",
    2: "fevereiro",
    3: "março",
    4: "abril",
    5: "maio",
    6: "junho",
    7: "julho",
    8: "agosto",
    9: "setembro",
    10: "outubro",
    11: "novembro",
    12: "dezembro"
}

class PostController:
    """Processes post content with mixed markdown and image elements."""

    def __init__(self, backend):
        self.backend = backend

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
                figure = soup.new_tag('figure', **{'class': 'article-image-figure'})

                img = soup.new_tag('img',
                                  src='/' + item['path'],
                                  alt=item.get('description', ''),
                                  **{'class': 'article-image'})
                figure.append(img)

                if item.get('legend'):
                    figcaption = soup.new_tag('figcaption', **{'class': 'article-image-caption'})
                    figcaption.string = item['legend']
                    figure.append(figcaption)

                soup.append(figure)

        return str(soup)

    def process_date(self, date: datetime.date):
        """Converts YYYY-MM-DD date to human readable date"""
        return f'{date.day} de {dict_mes[date.month]} de {date.year}'

    def run(self, document: dict) -> Post:
        """Process raw post content into a Post entity."""
        processed_content = self._process_content(document['content'])
        return Post(
            title=document.get('title', ''),
            content=processed_content,
            description=document.get('description', ''),
            date=self.process_date(document.get('date', '')),
            author=document.get('author', {}),
            banner=document.get('banner', ''),
            slug=document.get('slug', ''),
            tags=document.get('tags', []),
    )
