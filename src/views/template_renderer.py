"""Shared template renderer utility for functional views."""
from jinja2 import Environment, FileSystemLoader
from config import AppConfig

class TemplateRenderer:
    """Singleton template renderer for reuse across functional views."""
    _instance = None

    def __init__(self):
        if not hasattr(self, 'template_env'):
            config = AppConfig()
            self.template_env = Environment(
                loader=FileSystemLoader(config.get('searchpath', 'templates'))
            )
            self.cdn_url = config.get('static_url', '')

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def render_template(self, template_name: str, **kwargs):
        """Render a template with the given context."""
        template = self.template_env.get_template(template_name)
        return template.render(cdn_url=self.cdn_url, **kwargs)

# Create a shared instance for easy importing
template_renderer = TemplateRenderer()
