"""Unit tests for the MarkdownInterpreter module."""
import unittest
from parsers import parse_markdown


class TestMarkdownInterpreter(unittest.TestCase):
    """Test cases for MarkdownInterpreter class."""

    def test_interpret_simple_paragraph(self):
        """Test interpreting a simple paragraph."""
        markdown_text = "This is a paragraph."
        result = parse_markdown(markdown_text)
        self.assertIn('article-paragraph', result)
        self.assertIn('This is a paragraph.', result)

    def test_interpret_heading_1(self):
        """Test interpreting H1 heading."""
        markdown_text = "# Heading 1"
        result = parse_markdown(markdown_text)
        self.assertIn('article-heading-1', result)
        self.assertIn('Heading 1', result)

    def test_interpret_heading_2(self):
        """Test interpreting H2 heading."""
        markdown_text = "## Heading 2"
        result = parse_markdown(markdown_text)
        self.assertIn('article-heading-2', result)
        self.assertIn('Heading 2', result)

    def test_interpret_heading_3(self):
        """Test interpreting H3 heading."""
        markdown_text = "### Heading 3"
        result = parse_markdown(markdown_text)
        self.assertIn('article-heading-3', result)
        self.assertIn('Heading 3', result)

    def test_interpret_unordered_list(self):
        """Test interpreting unordered list."""
        markdown_text = "- Item 1\n- Item 2\n- Item 3"
        result = parse_markdown(markdown_text)
        self.assertIn('article-list', result)
        self.assertIn('article-list-item', result)
        self.assertIn('Item 1', result)
        self.assertIn('Item 2', result)

    def test_interpret_ordered_list(self):
        """Test interpreting ordered list."""
        markdown_text = "1. First\n2. Second\n3. Third"
        result = parse_markdown(markdown_text)
        self.assertIn('article-list', result)
        self.assertIn('article-list-item', result)
        self.assertIn('First', result)
        self.assertIn('Second', result)

    def test_interpret_link(self):
        """Test interpreting a link."""
        markdown_text = "[Example](https://example.com)"
        result = parse_markdown(markdown_text)
        self.assertIn('article-link', result)
        self.assertIn('https://example.com', result)
        self.assertIn('Example', result)

    def test_interpret_empty_string(self):
        """Test interpreting an empty string."""
        result = parse_markdown("")
        self.assertIsInstance(result, str)
        self.assertEqual(result.strip(), "")

    def test_interpret_complex_markdown(self):
        """Test interpreting complex markdown with multiple elements."""
        markdown_text = """# Main Title
        
This is a paragraph with [a link](https://example.com).

## Subsection

- Item 1
- Item 2

Another paragraph."""
        result = parse_markdown(markdown_text)
        self.assertIn('article-heading-1', result)
        self.assertIn('article-heading-2', result)
        self.assertIn('article-paragraph', result)
        self.assertIn('article-list', result)
        self.assertIn('article-link', result)


if __name__ == '__main__':
    unittest.main()
