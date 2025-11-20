"""Renders the article.html template with provided context."""
from bs4 import BeautifulSoup
from jinja2 import FileSystemLoader, Environment

class ArticleRenderer:
    """Renders the article.html template with provided context."""
    def __init__(self, config):
        searchpath, static_url = config['searchpath'], config['static_url']
        template_name = 'article.html'

        self.template_env = Environment(loader=FileSystemLoader(searchpath=searchpath))
        self.template = self.template_env.get_template(template_name)
        self.static_url = static_url

    def render(self, title, content: BeautifulSoup, description="", date=None, url="", author=None, banner=None, tags=[]):
        """Render the template with the given context."""
        return self.template.render(
            static_url=self.static_url,
            title=title,
            content=str(content),
            description=description,
            date=date,
            url=url,
            author=author,
            banner=banner,
            tags=tags
        )
