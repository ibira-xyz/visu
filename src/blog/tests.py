"""Unit tests for the blog app."""
from django.test import TestCase, RequestFactory
from blog.views import index


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
