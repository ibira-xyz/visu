"""A simple local server for development and testing purposes."""
from flask import Flask
from lorem_text import lorem
from yaml import load, SafeLoader

from renderers import IndexRenderer, ArticleRenderer
from interpreters.markdown import MarkdownInterpreter
from readers.local_reader import LocalReader 

app = Flask(__name__)

with open("config/local.yaml", "r", encoding="utf-8") as f:
    config = load(f, Loader=SafeLoader)

@app.route("/")
def home():
    """Route handler for the home page"""
    return IndexRenderer(config).render(
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

@app.route("/article")
def article():
    """Route handler for a sample article page"""
    
    return ArticleRenderer(config).render(
        title="Particionando o Espaço de Entrada em Redes Neurais",
        content=MarkdownInterpreter().interpret(LocalReader("static/assets/content.md").read()),
        description="Um artigo sobre particionamento de espaço em redes neurais",
        date="12 de novembro de 2025"
    )


if __name__ == "__main__":
    app.run(port=5000, debug=True)
