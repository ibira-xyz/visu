"""AWS Lambda handler for the home route"""
from yaml import load, SafeLoader

from renderers import IndexRenderer

with open("config.yaml", "r", encoding="utf-8") as f:
    config = load(f, Loader=SafeLoader)


def handler(_context, _event):
    """AWS Lambda handler function"""
    html_content = IndexRenderer(config).render()
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/html'
        },
        'body': html_content
    }

