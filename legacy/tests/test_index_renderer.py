"""Unit tests for the IndexView module."""
import unittest
import tempfile
import os
from views import IndexView


class TestIndexRenderer(unittest.TestCase):
    """Test cases for IndexRenderer class."""

    def setUp(self):
        """Set up test fixtures with a temporary template directory."""
        # Create a temporary directory for templates
        self.temp_dir = tempfile.mkdtemp()
        
        # Create a simple index.html template
        self.template_content = """<!DOCTYPE html>
<html>
<head>
    <title>Index</title>
    <link rel="stylesheet" href="{{ static_url }}/style.css">
</head>
<body>
    {% if feat %}
    <section class="featured">
        <h2>{{ feat.title }}</h2>
        <p>{{ feat.description }}</p>
    </section>
    {% endif %}
    
    {% if items %}
    <section class="items">
        <ul>
        {% for item in items %}
            <li>
                <a href="{{ item.url }}">{{ item.title }}</a>
                {% if item.date %}<time>{{ item.date }}</time>{% endif %}
            </li>
        {% endfor %}
        </ul>
    </section>
    {% endif %}
</body>
</html>"""
        
        template_path = os.path.join(self.temp_dir, 'index.html')
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(self.template_content)
        
        # Set up config
        self.config = {
            'searchpath': self.temp_dir,
            'static_url': '/static'
        }

    def tearDown(self):
        """Clean up temporary files."""
        template_path = os.path.join(self.temp_dir, 'index.html')
        if os.path.exists(template_path):
            os.unlink(template_path)
        if os.path.exists(self.temp_dir):
            os.rmdir(self.temp_dir)

    def test_init_with_config(self):
        """Test initialization with configuration."""
        renderer = IndexRenderer(self.config)
        self.assertEqual(renderer.static_url, '/static')
        self.assertIsNotNone(renderer.template)
        self.assertIsNotNone(renderer.template_env)

    def test_render_empty_index(self):
        """Test rendering an empty index."""
        renderer = IndexView()
        result = renderer.render()
        self.assertIn("<!DOCTYPE html>", result)
        self.assertIn("/static", result)

    def test_render_with_items_only(self):
        """Test rendering with only items list."""
        view = IndexView()
        items = [
            {'title': 'Post 1', 'url': '/post1'},
            {'title': 'Post 2', 'url': '/post2'},
            {'title': 'Post 3', 'url': '/post3'}
        ]
        result = view.render(items=items)
        self.assertIn('Post 1', result)
        self.assertIn('Post 2', result)
        self.assertIn('Post 3', result)
        self.assertIn('/post1', result)
        self.assertIn('/post2', result)

    def test_render_with_feat_and_items(self):
        """Test rendering with both featured item and items list."""
        renderer = IndexRenderer(self.config)
        feat = {
            'title': 'Featured Post',
            'description': 'Featured description'
        }
        items = [
            {'title': 'Post 1', 'url': '/post1'},
            {'title': 'Post 2', 'url': '/post2'}
        ]
        result = renderer.render(feat=feat, items=items)
        self.assertIn('Featured Post', result)
        self.assertIn('Featured description', result)
        self.assertIn('Post 1', result)
        self.assertIn('Post 2', result)

    def test_render_items_with_dates(self):
        """Test rendering items with date information."""
        renderer = IndexRenderer(self.config)
        items = [
            {'title': 'Recent Post', 'url': '/recent', 'date': '2024-01-15'},
            {'title': 'Old Post', 'url': '/old', 'date': '2023-12-01'}
        ]
        result = renderer.render(items=items)
        self.assertIn('2024-01-15', result)
        self.assertIn('2023-12-01', result)
        self.assertIn('<time>', result)

    def test_render_items_without_dates(self):
        """Test rendering items without date information."""
        renderer = IndexRenderer(self.config)
        items = [
            {'title': 'Undated Post', 'url': '/undated'}
        ]
        result = renderer.render(items=items)
        self.assertIn('Undated Post', result)
        # Should not have time tags for items without dates
        result_lines = [line for line in result.split('\n') if 'Undated Post' in line]
        for line in result_lines:
            if 'Undated Post' in line and '</li>' in line:
                self.assertNotIn('<time>', line)

    def test_static_url_in_output(self):
        """Test that static_url is correctly included in output."""
        custom_config = {
            'searchpath': self.temp_dir,
            'static_url': '/custom/assets'
        }
        renderer = IndexRenderer(custom_config)
        result = renderer.render()
        self.assertIn('/custom/assets', result)

    def test_render_with_empty_lists(self):
        """Test rendering with empty feat and items."""
        renderer = IndexRenderer(self.config)
        result = renderer.render(feat=None, items=[])
        self.assertIsInstance(result, str)
        self.assertIn('<!DOCTYPE html>', result)


if __name__ == '__main__':
    unittest.main()
