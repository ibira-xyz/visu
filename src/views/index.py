"""Functional index view using shared template renderer."""
from views.template_renderer import template_renderer

def render_index(context=None):
    """Render the index.html template with provided context."""
    return template_renderer.render_template('index.html', items=context)