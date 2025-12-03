"""AWS Lambda handler for the home route"""
from backend import get_backend
from controllers import IndexController, PostController
from views import IndexView, ArticleView

backend = get_backend()
index_controller = IndexController()
index_view = IndexView()

post_controller = PostController(backend)
article_view = ArticleView()


def handler_index(_context, _event):
    """AWS Lambda handler function"""
    html_content = index_view.render(
        **index_controller.run(
            backend.fetch_index_data()
        )
    )
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/html'
        },
        'body': html_content
    }
