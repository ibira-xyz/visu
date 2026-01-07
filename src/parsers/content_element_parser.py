"""Parser for replacing placeholders in post content with HTML elements."""
from re import Match
from bs4 import BeautifulSoup

from config.app_config import AppConfig
config = AppConfig()


class ContentElementParser:
    """Class to parse content elements in post content."""
    def __init__(self, content_elements: list):
        self.elements_by_id = {item.get('id'): item for item in content_elements if item.get('id')}
        self.cdn_url = config.get('static_url')
        self.component_scripts = []
        self.placeholder_pattern = r'\{\{\s*([^}]+)\s*\}\}'

    def replace_placeholder(self, match: Match) -> str:
        """Replace placeholder with corresponding content element HTML."""
        item_id = match.group(1).strip()
        if item_id in self.elements_by_id:
            item = self.elements_by_id[item_id]
            return self.create_content_element_html(item)
        else:
            return match.group(0)

    def create_content_element_html(self, item: dict) -> str:
        """Create HTML for a single content element."""
        soup = BeautifulSoup("", "html.parser")
        item_type = item.get('type')

        if item_type == 'image':
            soup = self.parse_figure(item)

        elif item_type == 'component':
            soup = self.parse_component(item)

        return str(soup)

    def parse_figure(self, item: dict) -> BeautifulSoup:
        """Parse figure elements from a content item."""
        soup = BeautifulSoup("", "html.parser")
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

        return figure

    def parse_component(self, item: dict) -> BeautifulSoup:
        """Parse interactive component elements from a content item."""
        soup = BeautifulSoup("", "html.parser")
        container_id = item.get('id', f'component-{hash(str(item))}')
        component_div = soup.new_tag('div', **{
            'id': container_id,
            'class': 'post-component',
            'data-component-script': item.get('script', '')
        })

        # Add any custom data attributes
        if 'data' in item:
            for key, value in item['data'].items():
                component_div[f'data-{key}'] = str(value)

        # Optional caption/description
        if item.get('caption'):
            figure = soup.new_tag('figure', **{'class': 'post-component-figure'})
            figure.append(component_div)
            figcaption = soup.new_tag('figcaption', **{'class': 'post-component-caption'})
            figcaption.string = item['caption']
            figure.append(figcaption)
            soup.append(figure)
        else:
            soup.append(component_div)

        if item.get('script'):
            self.component_scripts.append(item['script'])

        return soup
