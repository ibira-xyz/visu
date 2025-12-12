"""Functional post view using shared template renderer."""
from views.template_renderer import template_renderer

def render_post(context=None):
    """Render the post.html template with provided context."""
    return template_renderer.render_template('post.html',
                                             slug=context.slug,
                                             title=context.title,
                                             content=context.content,
                                             description=context.description,
                                             date=context.date,
                                             author=context.author,
                                             banner=context.banner,
                                             tags=context.tags
    )