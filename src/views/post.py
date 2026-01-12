"""Functional post view using shared template renderer."""
from views.template_renderer import template_renderer

def render_post(post=None, formatted_date=None, post_content=None) -> str:
    """Render the post.html template with provided context."""
    return template_renderer.render_template('post.html',
                                             post=post,
                                             formatted_date=formatted_date,
                                             post_content=post_content
    )
