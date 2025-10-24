"""A simple local server for development and testing purposes."""
from flask import Flask
from yaml import load, SafeLoader

from renderers import IndexRenderer

app = Flask(__name__)

with open("config/local.yaml", "r", encoding="utf-8") as f:
    config = load(f, Loader=SafeLoader)

@app.route("/")
def home():
    """Route handler for the home page"""
    return IndexRenderer(config).render(items=[{
        "title": "Sample Item",
        "description": "This is a description for a sample item.",
        "image_url": "sample.jpg",
        "link": "https://example.com"
    }]*5)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
