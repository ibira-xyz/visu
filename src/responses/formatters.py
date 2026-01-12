"""Module providing response formatters for different frameworks"""

def flask_response(content, status_code):
    """Helper function to create a Flask Response"""
    return content,status_code

def lambda_response(content, status_code):
    """Helper function to create a Lambda HTTP response"""
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'text/html'
        },
        'body': content
    }