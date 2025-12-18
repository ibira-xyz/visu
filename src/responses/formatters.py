from flask import Response

def flask_response(content, status_code):
    """Helper function to create a Flask Response"""
    return Response(response=content, status=status_code, mimetype='text/html')

def lambda_response(content, status_code):
    """Helper function to create a Lambda HTTP response"""
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'text/html'
        },
        'body': content
    }