"""AWS Lambda handler for the home route"""
from backend import get_backend
from controllers import post_controller
from views import render_post, render_not_found, render_server_error
from decorators import safe_response

backend = get_backend()

@safe_response
def handler(event, _context):
    """AWS Lambda handler function for post pages"""
    path_params = event.get('pathParameters') or {}
    slug = path_params.get('slug')
    html_content = render_post(
        **post_controller.process_post(
            backend.get_post(slug),
            backend
        )
    )
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/html'
        },
        'body': html_content
    }
