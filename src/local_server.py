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
    return IndexRenderer(config).render()


if __name__ == "__main__":
    app.run(port=5000, debug=True)
