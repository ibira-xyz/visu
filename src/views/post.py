"""Functional post view using shared template renderer."""
from views.template_renderer import template_renderer

def render_post(post=None, post_content=None):
    """Render the post.html template with provided context."""
    return template_renderer.render_template('post.html',
                                             post=post,
                                             post_content=post_content
    )