"""Markdown Interpreter Module"""
from markdown import markdown
from bs4 import BeautifulSoup

SEMANTIC_CLASSES = {
    "p": "post-paragraph",
    "h1": "post-heading-1",
    "h2": "post-heading-2",
    "h3": "post-heading-3",
    "ul": "post-list",
    "ol": "post-list",
    "li": "post-list-item",
    "a": "post-link",
}

def parse_markdown(markdown_text: str) -> str:
    """Convert markdown text to HTML with semantic CSS classes."""
    # Convert markdown to HTML
    html = markdown(markdown_text)
    # Use BeautifulSoup to add semantic classes
    soup = BeautifulSoup(html, features="html.parser")
    for tag, css_class in SEMANTIC_CLASSES.items():
        for element in soup.find_all(tag):
            element['class'] = css_class
    return str(soup)
