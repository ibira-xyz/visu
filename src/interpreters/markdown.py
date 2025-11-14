"""Markdown Interpreter Module"""
from markdown import markdown
from bs4 import BeautifulSoup

class MarkdownInterpreter:
    """Interpreter for converting markdown text to plain text."""
    def __init__(self, style=None):
        self.style = style

    def interpret(self, markdown_text):
        """Convert markdown text to plain text."""
        # Convert markdown to HTML
        html = markdown(markdown_text)
        # Use BeautifulSoup to extract plain text from HTML
        soup = BeautifulSoup(html, features="html.parser")
        for tag in self.style.get_tags():
            for element in soup.find_all(tag):
                element['class'] = self.style.get_class(tag)
        print(soup.prettify())
        return soup
