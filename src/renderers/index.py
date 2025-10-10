"""Renders the index.html template with provided context."""
from jinja2 import FileSystemLoader, Environment

class IndexRenderer:
    """Renders the index.html template with provided context."""
    def __init__(self, config):
        searchpath, static_url = config['searchpath'], config['static_url']
        template_name = 'index.html'

        self.template_env = Environment(loader=FileSystemLoader(searchpath=searchpath))
        self.template = self.template_env.get_template(template_name)
        self.static_url = static_url

    def render(self):
        """Render the template with the given context."""
        return self.template.render(static_url=self.static_url)
