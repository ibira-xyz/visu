"""A simple local server for development and testing purposes."""
from flask import Flask
from lorem_text import lorem
from yaml import load, SafeLoader

from views import IndexView, ArticleView
from controllers import PostController
from backend import get_backend

app = Flask(__name__, static_folder='static', static_url_path='/static')

with open("config/local.yaml", "r", encoding="utf-8") as f:
    config = load(f, Loader=SafeLoader)

backend = get_backend(config)
article_view = ArticleView(config['searchpath'])
post_controller = PostController(backend)
index_view = IndexView(config['searchpath'])

@app.route("/")
def home():
    """Route handler for the home page"""
    return index_view.render(
        items=[{
        "title": "Particionando o Espaço de Entrada em Redes Neurais",
        "description": lorem.words(25),
        "image": "drawing.svg",
        "link": "https://google.com"
    }, {
        "title": "Sample Item 2",
        "description": lorem.words(20),
        "image": "drawing.svg",
        "link": "https://example.com"
    }, {
        "title": "Sample Item 3",
        "description": lorem.words(20),
        "image": "drawing.svg",
        "link": "https://example.com"
    }]
    )

@app.route("/post/<slug>")
def article(slug):
    """Route handler for a sample article page"""
    return article_view.render(
        post_controller.run(
            backend.get_post(slug))
        )

if __name__ == "__main__":
    app.run(port=5000, debug=True)
