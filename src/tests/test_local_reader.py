"""Unit tests for the LocalReader module."""
import unittest
import tempfile
import os
from readers.local_reader import LocalReader


class TestLocalReader(unittest.TestCase):
    """Test cases for LocalReader class."""

    def setUp(self):
        """Set up test fixtures with temporary files."""
        self.test_content = "This is test content.\nWith multiple lines."
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8')
        self.temp_file.write(self.test_content)
        self.temp_file.close()
        self.temp_file_path = self.temp_file.name

    def tearDown(self):
        """Clean up temporary files."""
        if os.path.exists(self.temp_file_path):
            os.unlink(self.temp_file_path)

    def test_init_with_file_path(self):
        """Test initialization with a file path."""
        reader = LocalReader(self.temp_file_path)
        self.assertEqual(reader.file_path, self.temp_file_path)

    def test_read_file_content(self):
        """Test reading content from a file."""
        reader = LocalReader(self.temp_file_path)
        content = reader.read()
        self.assertEqual(content, self.test_content)

    def test_read_empty_file(self):
        """Test reading an empty file."""
        empty_file = tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8')
        empty_file.close()
        try:
            reader = LocalReader(empty_file.name)
            content = reader.read()
            self.assertEqual(content, "")
        finally:
            os.unlink(empty_file.name)

    def test_read_unicode_content(self):
        """Test reading Unicode content."""
        unicode_content = "Hello 世界! 🌍"
        unicode_file = tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8')
        unicode_file.write(unicode_content)
        unicode_file.close()
        try:
            reader = LocalReader(unicode_file.name)
            content = reader.read()
            self.assertEqual(content, unicode_content)
        finally:
            os.unlink(unicode_file.name)

    def test_read_nonexistent_file(self):
        """Test reading a non-existent file raises FileNotFoundError."""
        reader = LocalReader('/path/to/nonexistent/file.txt')
        with self.assertRaises(FileNotFoundError):
            reader.read()

    def test_read_multiple_times(self):
        """Test that reading multiple times returns the same content."""
        reader = LocalReader(self.temp_file_path)
        content1 = reader.read()
        content2 = reader.read()
        self.assertEqual(content1, content2)

    def test_read_multiline_content(self):
        """Test reading multiline content preserves line breaks."""
        multiline_content = "Line 1\nLine 2\nLine 3"
        multiline_file = tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8')
        multiline_file.write(multiline_content)
        multiline_file.close()
        try:
            reader = LocalReader(multiline_file.name)
            content = reader.read()
            self.assertEqual(content, multiline_content)
            self.assertEqual(content.count('\n'), 2)
        finally:
            os.unlink(multiline_file.name)


if __name__ == '__main__':
    unittest.main()
