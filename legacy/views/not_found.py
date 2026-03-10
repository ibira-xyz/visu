"""Functional not found view using shared template renderer."""
from views.template_renderer import template_renderer

def render_not_found() -> str:
    """Render the not_found.html template with provided context."""
    return template_renderer.render_template('not_found.html')
