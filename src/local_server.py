"""A simple local server for development and testing purposes."""
from flask import Flask

from views import render_index, render_post
from controllers import post_controller, index_controller
from backend import get_backend

app = Flask(__name__, static_folder='static', static_url_path='/static')

backend = get_backend()

@app.route("/")
def home():
    """Route handler for the home page"""
    return render_index(
        **index_controller.process_posts(
            backend.get_all_posts()
        )
    )

@app.route("/post/<slug>")
def post(slug):
    """Route handler for a sample post page"""
    return render_post(
        **post_controller.process_post(
            backend.get_post(slug),
            backend)
        )

if __name__ == "__main__":
    app.run(port=5000, debug=True)
