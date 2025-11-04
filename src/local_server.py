"""A simple local server for development and testing purposes."""
from flask import Flask
from lorem_text import lorem
from yaml import load, SafeLoader

from renderers import IndexRenderer

app = Flask(__name__)

with open("config/local.yaml", "r", encoding="utf-8") as f:
    config = load(f, Loader=SafeLoader)

@app.route("/")
def home():
    """Route handler for the home page"""
    return IndexRenderer(config).render(feat={
        "title": "Featured Item",
        "description": lorem.words(50),
        "image_url": "drawing.svg",
        "link": "https://example.com/featured"
    },
        items=[{
        "title": "Sample Item",
        "description": lorem.words(20),
        "image_url": "drawing.svg",
        "link": "https://example.com"
    }]*5
    )


if __name__ == "__main__":
    app.run(port=5000, debug=True)
