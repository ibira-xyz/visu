"""Content parser for Lexical JSON to HTML conversion.
This module defines the ContentParser class, which takes Lexical
JSON content and converts it into HTML format. It handles various
node types such as headings, paragraphs, lists, quotes, code blocks,
and media blocks, applying appropriate formatting based on the
content's structure and formatting flags.
"""

import json
import logging
from django.core.exceptions import ObjectDoesNotExist
from django.utils.safestring import mark_safe
from ..models import Media

logger = logging.getLogger(__name__)

# Text format constants
IS_BOLD = 1
IS_ITALIC = 1 << 1
IS_STRIKETHROUGH = 1 << 2
IS_UNDERLINE = 1 << 3
IS_CODE = 1 << 4
IS_SUBSCRIPT = 1 << 5
IS_SUPERSCRIPT = 1 << 6

class ContentParser:
    """Parser for Lexical JSON content to HTML."""
    def __init__(self, content, cdn_url):
        if isinstance(content, str):
            try:
                self.root = json.loads(content).get('root', {})
            except json.JSONDecodeError:
                logger.error("Failed to parse content JSON.")
                self.root = {}
        else:
            self.root = content.get('root', {}) if content else {}

        self.component_scripts = []
        self.cdn_url = cdn_url

    def parse(self):
        """Parse the content and return HTML."""
        if not self.root:
            return ""

        parts = []
        children = self.root.get('children', [])

        # Se isso virar gargalo, podemos otimizar paralelizando a renderização dos nós filhos.
        for child in children:
            parts.append(self.render_node(child))

        return mark_safe("".join(parts))

    def render_node(self, node):
        """Render a single node based on its type and content."""
        node_type = node.get('type')

        if node_type == 'heading':
            tag = node.get('tag')
            if tag not in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                logger.warning("Invalid heading tag '%s' found. Defaulting to 'h1'.", tag)
                tag = 'h1'  # Default to h1 if tag is missing or invalid

            content = self.render_children(node)
            return f'<{tag}>{content}</{tag}>'

        elif node_type == 'paragraph':
            # Check for component placeholder
            children = node.get('children', [])
            content = self.render_children(node)
            if not content.strip() and not children:
                return '<br>'
            return f'<p>{content}</p>'

        elif node_type == 'list':
            tag = node.get('tag')
            if tag not in ['ul', 'ol']:
                logger.warning("Invalid list tag '%s' found. Defaulting to 'ul'.", tag)
                tag = 'ul'  # Default to ul if tag is missing or invalid

            content = self.render_children(node)
            return f'<{tag}>{content}</{tag}>'

        elif node_type == 'listitem':
            content = self.render_children(node)
            return f'<li>{content}</li>'

        elif node_type == 'quote':
            content = self.render_children(node)
            return f'<blockquote>{content}</blockquote>'

        elif node_type == 'block':
            fields = node.get('fields', {})
            if fields.get('blockType') == 'mediaBlock':
                return self.render_media_block(fields)
            return ""

        elif node_type == 'text':
            text = node.get('text', '')
            format_flags = node.get('format', 0)
            return self.apply_formatting(text, format_flags)

        elif node_type == 'link':
            url = node.get('fields', {}).get('url') or node.get('url', '#')
            content = self.render_children(node)
            new_tab = node.get('fields', {}).get('newTab', False)
            target_attr = ' target="_blank" rel="noopener noreferrer"' if new_tab else ''
            return f'<a href="{url}"{target_attr}>{content}</a>'

        return ""

    def render_children(self, node):
        """Render all child nodes and concatenate their HTML."""
        return "".join([self.render_node(child) for child in node.get('children', [])])

    def apply_formatting(self, text, flags):
        """Apply text formatting based on the provided flags."""
        if flags & IS_BOLD:
            text = f'<strong>{text}</strong>'
        if flags & IS_ITALIC:
            text = f'<em>{text}</em>'
        if flags & IS_STRIKETHROUGH:
            text = f'<del>{text}</del>'
        if flags & IS_UNDERLINE:
            text = f'<u>{text}</u>'
        if flags & IS_CODE:
            text = f'<code>{text}</code>'
        if flags & IS_SUBSCRIPT:
            text = f'<sub>{text}</sub>'
        if flags & IS_SUPERSCRIPT:
            text = f'<sup>{text}</sup>'
        return text

    def render_media_block(self, fields):
        """Render a media block based on the provided fields."""
        try:
            media_id = fields.get('media')
            if media_id:
                media = Media.objects.get(id=media_id)

                alt_text = media.alt if media.alt else ''
                caption = ''
                # Attempt to extract caption text if it's stored as Lexical JSON
                if media.caption:
                    if isinstance(media.caption, dict):
                        try:
                            caption = media.caption \
                                .get('root', {}) \
                                .get('children', [])[0] \
                                .get('children', [])[0] \
                                .get('text', '')
                        except (IndexError, AttributeError):
                            pass
                    elif isinstance(media.caption, str):
                        caption = media.caption

                return f'''
                <figure class="post-image-figure">
                    <img src="{self.cdn_url}{media.filename}" alt="{alt_text}" class="post-image" />
                    {f'<figcaption class="post-image-caption">{caption}</figcaption>'
                     if caption else ''}
                </figure>
                '''
        except ObjectDoesNotExist:
            logger.error("Media with ID '%s' not found.", media_id)
            return ""
        return ""

