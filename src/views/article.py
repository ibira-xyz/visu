"""Renders the article.html template with provided context."""
from models.post import Post
from views.view import View


class ArticleView(View):
    """Renders the article.html template with provided context."""
    def __init__(self):
        super().__init__()
        self.template = self.template_env.get_template('article.html')

    def render(self, context: Post):
        """Render the template with the given context."""
        return self.template.render(
            slug=context.slug,
            title=context.title,
            content=context.content,
            description=context.description,
            date=context.date,
            author=context.author,
            banner=context.banner,
            tags=context.tags
        )
