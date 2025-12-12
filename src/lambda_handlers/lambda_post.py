"""AWS Lambda handler for the home route"""
from backend import get_backend
from controllers import PostController
from views import render_post

backend = get_backend()

post_controller = PostController(backend)

def handler(event, _context):
    """AWS Lambda handler function for post pages"""
    path_params = event.get('pathParameters') or {}
    slug = path_params.get('slug')
    html_content = render_post(
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
