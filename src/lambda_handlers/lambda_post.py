"""AWS Lambda handler for the home route"""
from drivers import get_driver
from controllers import post_controller
from views import render_post
from responses import safe_response, lambda_response

driver = get_driver()

@safe_response(lambda_response)
def handler(event, _context):
    """AWS Lambda handler function for post pages"""
    path_params = event.get('pathParameters') or {}
    slug = path_params.get('slug')
    html_content = render_post(
        **post_controller.process_post(
            driver.get_post(slug),
            driver
        )
    )
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/html'
        },
        'body': html_content
    }
