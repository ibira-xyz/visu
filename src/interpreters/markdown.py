"""Markdown Interpreter Module"""
from markdown import markdown
from bs4 import BeautifulSoup

SEMANTIC_CLASSES = {
    "p": "article-paragraph",
    "h1": "article-heading-1",
    "h2": "article-heading-2",
    "h3": "article-heading-3",
    "ul": "article-list",
    "ol": "article-list",
    "li": "article-list-item",
    "a": "article-link",
}

class MarkdownInterpreter:
    """Interpreter for converting markdown text to HTML with semantic classes."""
    
    def interpret(self, markdown_text):
        """Convert markdown text to HTML with semantic CSS classes."""
        # Convert markdown to HTML
        html = markdown(markdown_text)
        # Use BeautifulSoup to add semantic classes
        soup = BeautifulSoup(html, features="html.parser")
        for tag, css_class in SEMANTIC_CLASSES.items():
            for element in soup.find_all(tag):
                element['class'] = css_class
        return str(soup)
