"""Controller for processing post content into Post entities."""

from bs4 import BeautifulSoup

from backend.backend import Backend
from config.app_config import AppConfig
from models import Post, PostContent
from parsers import parse_markdown, process_date

config = AppConfig()


def create_post_content(slug: str, content_items: list, backend: Backend) -> PostContent:
    """Process content items and return combined HTML."""
    soup = BeautifulSoup("", "html.parser")
    component_scripts = []
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

        elif item_type == 'component':
            # Create container div for interactive component
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

            # Collect component script
            if item.get('script'):
                component_scripts.append(item['script'])

    return PostContent(
        slug=slug,
        article=str(soup),
        component_scripts=component_scripts
    )

def process_post(post: Post, backend: Backend) -> dict:
    """Process raw post content into a Post entity."""
    return {'post': post,
            'post_content': create_post_content(post.slug, post.content_metadata, backend),
            'formatted_date': process_date(post.date)}
