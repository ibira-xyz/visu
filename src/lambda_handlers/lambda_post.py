"""AWS Lambda handler for the home route"""
from backend import get_backend
from controllers import IndexController, PostController
from views import IndexView, ArticleView

backend = get_backend()
index_controller = IndexController()
index_view = IndexView()

post_controller = PostController(backend)
article_view = ArticleView()

def handler(event, _context):
    """AWS Lambda handler function for article pages"""
    slug = event['pathParameters']['slug']
    html_content = article_view.render(
        post_controller.run(
            backend.get_post(slug))
        )
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/html'
        },
        'body': html_content
    }
