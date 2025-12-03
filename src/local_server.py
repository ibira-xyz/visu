"""A simple local server for development and testing purposes."""
from flask import Flask
from yaml import load, SafeLoader

from views import IndexView, ArticleView
from controllers import PostController, IndexController
from backend import get_backend

app = Flask(__name__, static_folder='static', static_url_path='/static')

with open("config/local.yaml", "r", encoding="utf-8") as f:
    config = load(f, Loader=SafeLoader)

backend = get_backend(config)

post_controller = PostController(backend)
article_view = ArticleView(config['searchpath'])

index_controller = IndexController(backend)
index_view = IndexView(config['searchpath'])

@app.route("/")
def home():
    """Route handler for the home page"""
    return index_view.render(
        **index_controller.run(
            backend.fetch_index_data()
        )
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
