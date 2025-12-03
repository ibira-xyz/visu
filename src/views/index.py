"""Renders the index.html template with provided context."""
from views.view import View

class IndexView(View):
    """Renders the index.html template with provided context."""
    def __init__(self, searchpath: str):
        super().__init__(searchpath)
        self.template = self.template_env.get_template('index.html')
    
    def render(self, items=None):
        """Render the template with the given context."""
        return self.template.render(items=items)
