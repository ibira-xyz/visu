"""Unit tests for the ArticleRenderer module."""
import unittest
import tempfile
import os
from bs4 import BeautifulSoup
from renderers.article import ArticleRenderer


class TestArticleRenderer(unittest.TestCase):
    """Test cases for ArticleRenderer class."""

    def setUp(self):
        """Set up test fixtures with a temporary template directory."""
        # Create a temporary directory for templates
        self.temp_dir = tempfile.mkdtemp()

        # Create a simple article.html template
        self.template_content = """<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
    <meta name="description" content="{{ description }}">
    <link rel="stylesheet" href="{{ static_url }}/style.css">
</head>
<body>
    <article>
        <h1>{{ title }}</h1>
        {% if date %}<time>{{ date }}</time>{% endif %}
        <div class="content">{{ content }}</div>
        {% if url %}<a href="{{ url }}">Link</a>{% endif %}
    </article>
</body>
</html>"""

        template_path = os.path.join(self.temp_dir, 'article.html')
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(self.template_content)

        # Set up config
        self.config = {
            'searchpath': self.temp_dir,
            'static_url': '/static'
        }

    def tearDown(self):
        """Clean up temporary files."""
        # Remove the template file and directory
        template_path = os.path.join(self.temp_dir, 'article.html')
        if os.path.exists(template_path):
            os.unlink(template_path)
        if os.path.exists(self.temp_dir):
            os.rmdir(self.temp_dir)

    def test_init_with_config(self):
        """Test initialization with configuration."""
        renderer = ArticleRenderer(self.config)
        self.assertEqual(renderer.static_url, '/static')
        self.assertIsNotNone(renderer.template)
        self.assertIsNotNone(renderer.template_env)

    def test_render_basic_article(self):
        """Test rendering a basic article."""
        renderer = ArticleRenderer(self.config)
        content = BeautifulSoup("<p>Article content</p>", 'html.parser')
        result = renderer.render(
            title="Test Article",
            content=content
        )
        self.assertIn("Test Article", result)
        self.assertIn("Article content", result)
        self.assertIn("/static", result)

    def test_render_with_all_parameters(self):
        """Test rendering with all parameters."""
        renderer = ArticleRenderer(self.config)
        content = BeautifulSoup("<p>Full content</p>", 'html.parser')
        result = renderer.render(
            title="Complete Article",
            content=content,
            description="Test description",
            date="2024-01-01",
            url="https://example.com"
        )
        self.assertIn("Complete Article", result)
        self.assertIn("Full content", result)
        self.assertIn("Test description", result)
        self.assertIn("2024-01-01", result)
        self.assertIn("https://example.com", result)

    def test_render_without_optional_parameters(self):
        """Test rendering without optional parameters."""
        renderer = ArticleRenderer(self.config)
        content = BeautifulSoup("<p>Minimal content</p>", 'html.parser')
        result = renderer.render(
            title="Minimal Article",
            content=content
        )
        self.assertIn("Minimal Article", result)
        self.assertIn("Minimal content", result)
        # Optional parameters should not appear
        self.assertNotIn("2024", result.split("<time>")[0] if "<time>" in result else result)

    def test_render_with_complex_content(self):
        """Test rendering with complex HTML content."""
        renderer = ArticleRenderer(self.config)
        content = BeautifulSoup(
            "<h2>Subtitle</h2><p>Paragraph 1</p><p>Paragraph 2</p>",
            'html.parser'
        )
        result = renderer.render(
            title="Complex Article",
            content=content
        )
        self.assertIn("Subtitle", result)
        self.assertIn("Paragraph 1", result)
        self.assertIn("Paragraph 2", result)

    def test_render_preserves_html_structure(self):
        """Test that rendering preserves HTML structure."""
        renderer = ArticleRenderer(self.config)
        content = BeautifulSoup("<div><ul><li>Item 1</li><li>Item 2</li></ul></div>", 'html.parser')
        result = renderer.render(
            title="List Article",
            content=content
        )
        self.assertIn("<ul>", result)
        self.assertIn("<li>", result)
        self.assertIn("Item 1", result)
        self.assertIn("Item 2", result)

    def test_static_url_in_output(self):
        """Test that static_url is correctly included in output."""
        custom_config = {
            'searchpath': self.temp_dir,
            'static_url': '/custom/static/path'
        }
        renderer = ArticleRenderer(custom_config)
        content = BeautifulSoup("<p>Content</p>", 'html.parser')
        result = renderer.render(title="Test", content=content)
        self.assertIn("/custom/static/path", result)


if __name__ == '__main__':
    unittest.main()
