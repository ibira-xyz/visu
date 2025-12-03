"""AWS Lambda handler for the home route"""
from backend import get_backend
from controllers import IndexController, PostController
from views import IndexView, PostView

backend = get_backend()
index_controller = IndexController()
index_view = IndexView()

post_controller = PostController(backend)
post_view = PostView()

def handler(event, _context):
    """AWS Lambda handler function for post pages"""
    path_params = event.get('pathParameters') or {}
    slug = path_params.get('slug')
    html_content = post_view.render(
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
