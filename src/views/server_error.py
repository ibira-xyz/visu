"""Functional server error view using shared template renderer."""
from views.template_renderer import template_renderer

def render_server_error() -> str:
    """Render the server_error.html template with provided context."""
    return template_renderer.render_template('server_error.html')
