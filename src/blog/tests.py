"""Unit tests for the blog app."""
from django.test import TestCase, RequestFactory
from blog.views import index
from blog.processors.content_parser import ContentParser


class TestIndexView(TestCase):
    """Test cases for the index view function."""

    def setUp(self):
        """Set up test fixtures."""
        self.factory = RequestFactory()

    def test_index_returns_response(self):
        """Test that index view returns a response."""
        request = self.factory.get('/')
        response = index(request)
        self.assertEqual(response.status_code, 200)


class TestContentParser(TestCase):
    """Test cases for ContentParser output."""

    def test_latex_block_renders_placeholder_with_escaped_content(self):
        """LaTeX blocks are emitted for client-side KaTeX with safe escaped fallback."""
        content = {
            'root': {
                'children': [
                    {
                        'type': 'block',
                        'fields': {
                            'blockType': 'latex',
                            'latex': r'\\frac{a}{b} < c',
                        },
                    }
                ]
            }
        }

        parser = ContentParser(content, 'https://cdn.example/')
        rendered = str(parser.parse())

        self.assertIn('latex-block', rendered)
        self.assertIn('data-latex="\\\\frac{a}{b} &lt; c"', rendered)
        self.assertIn('>\\\\frac{a}{b} &lt; c<', rendered)
        self.assertNotIn('< c', rendered)
        self.assertIn('displayMode', rendered)

    def test_empty_latex_block_renders_nothing(self):
        """Empty latex values produce no output."""
        content = {
            'root': {
                'children': [
                    {
                        'type': 'block',
                        'fields': {
                            'blockType': 'latex',
                            'latex': '',
                        },
                    }
                ]
            }
        }

        parser = ContentParser(content, 'https://cdn.example/')
        rendered = str(parser.parse())

        self.assertEqual(rendered, '')
    
    def test_latex_inline_renders_placeholder_with_escaped_content(self):
        """LaTeX inline blocks are emitted for client-side
        KaTeX with safe escaped fallback."""
        content = {
            'root': {
                'children': [
                    {
                        'type': 'inlineLatex',
                        'latex': r'\\frac{a}{b} < c',
                    }
                ]
            }
        }

        parser = ContentParser(content, 'https://cdn.example/')
        rendered = str(parser.parse())

        self.assertIn('latex-block', rendered)
        self.assertIn('data-latex="\\\\frac{a}{b} &lt; c"', rendered)
        self.assertIn('>\\\\frac{a}{b} &lt; c<', rendered)
        self.assertNotIn('< c', rendered)
        self.assertNotIn('displayMode', rendered)

    def test_empty_latex_inline_renders_nothing(self):
        """Empty latex inline values produce no output."""
        content = {
            'root': {
                'children': [
                    {
                        'type': 'inlineLatex',
                        'latex': '',
                    }
                ]
            }
        }

        parser = ContentParser(content, 'https://cdn.example/')
        rendered = str(parser.parse())

        self.assertEqual(rendered, '')
