"""A simple local server for development and testing purposes."""
from flask import Flask

from views import render_index, render_post
from controllers import post_controller, index_controller
from drivers import get_driver
from responses import safe_response, flask_response

app = Flask(__name__, static_folder='static', static_url_path='/static')

driver = get_driver()

@app.route("/")
@safe_response(flask_response)
def home():
    """Route handler for the home page"""
    return render_index(
        **index_controller.process_posts(
            driver.get_all_posts()
        )
    )

@app.route("/post/<slug>")
@safe_response(flask_response)
def post(slug):
    """Route handler for a sample post page"""
    return render_post(
        **post_controller.process_post(
            driver.get_post(slug),
            driver)
        )

if __name__ == "__main__":
    app.run(port=8080, debug=True)
