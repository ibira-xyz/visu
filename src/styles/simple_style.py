"""Simple Style Module"""
from styles.base_style import BaseStyle

CLASSES_MAPPING = {
    "p": "text-dark-moss-gree indent-8 text-justify",
    "h1": "text-dark-moss-green",
    "h2": "text-cordovan-400 font-bold mt-8 mb-4",
    "h3": "text-dark-moss-green",
    "ul": "text-dark-moss-green",
    "ol": "text-dark-moss-green",
    "li": "text-dark-moss-green",
    "a": "text-dark-moss-green-600 hover:underline",
}

class SimpleStyle(BaseStyle):
    """Simple style implementation."""
    def get_tags(self):
        return ["p", "h1", "h2", "h3", "ul", "ol", "li", "a"]
    def get_class(self, tag):
        return CLASSES_MAPPING.get(tag, "")