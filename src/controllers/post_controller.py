"""Controller for processing post content into Post entities."""

import re
from bs4 import BeautifulSoup

from backend.backend import Backend
from config.app_config import AppConfig
from models import Post, PostContent
from parsers import parse_markdown, process_date

config = AppConfig()


def create_content_element_html(item: dict, cdn_url: str) -> str:
    """Create HTML for a single content element."""
    soup = BeautifulSoup("", "html.parser")
    item_type = item.get('type')

    if item_type == 'image':
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

    return str(soup)


def create_post_content(slug: str, content: str, content_elements: list, backend: Backend) -> PostContent:
    """Process content items and return combined HTML with placeholder substitution."""
    component_scripts = []
    cdn_url = config.get('static_url')
    markdown_content = backend.get_content(content)
    html = parse_markdown(markdown_content)
    
    # Create a mapping of element IDs to element configs
    elements_by_id = {item.get('id'): item for item in content_elements if item.get('id')}
    
    # Find and replace all placeholders in the HTML
    def replace_placeholder(match):
        item_id = match.group(1).strip()
        if item_id in elements_by_id:
            item = elements_by_id[item_id]
            
            # Collect component script if it's a component
            if item.get('type') == 'component' and item.get('script'):
                component_scripts.append(item['script'])
                
            return create_content_element_html(item, cdn_url)
        else:
            # Return the original placeholder if no matching element found
            return match.group(0)
    
    # Replace placeholders with pattern {{ item_id }}
    placeholder_pattern = r'\{\{\s*([^}]+)\s*\}\}'
    processed_html = re.sub(placeholder_pattern, replace_placeholder, html)

    return PostContent(
        slug=slug,
        article=processed_html,
        component_scripts=component_scripts
    )

def process_post(post: Post, backend: Backend) -> dict:
    """Process raw post content into a Post entity."""
    return {'post': post,
            'post_content': create_post_content(post.slug,
                                                post.content,
                                                post.content_elements,
                                                backend),
            'formatted_date': process_date(post.date)}
