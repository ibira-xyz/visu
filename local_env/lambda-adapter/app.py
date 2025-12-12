"""
Lambda Adapter - Converte requisições HTTP em eventos Lambda
Simula o comportamento do API Gateway AWS
"""
from flask import Flask, request, Response
import requests
import json

app = Flask(__name__)

LAMBDA_ENDPOINTS = {
    'index': 'http://lambda-index:8080/2015-03-31/functions/function/invocations',
    'post': 'http://lambda-post:8080/2015-03-31/functions/function/invocations'
}

@app.route('/invoke/index', methods=['GET', 'POST'])
def invoke_index():
    """Invoca a Lambda de index"""
    event = {}
    
    response = requests.post(
        LAMBDA_ENDPOINTS['index'],
        json=event,
        headers={'Content-Type': 'application/json'}
    )
    
    lambda_response = response.json()
    return Response(
        lambda_response.get('body', ''),
        status=lambda_response.get('statusCode', 200),
        headers=lambda_response.get('headers', {})
    )

@app.route('/invoke/post/<slug>', methods=['GET', 'POST'])
def invoke_post(slug):
    """Invoca a Lambda de post com o slug"""
    event = {
        'pathParameters': {
            'slug': slug
        }
    }
    
    response = requests.post(
        LAMBDA_ENDPOINTS['post'],
        json=event,
        headers={'Content-Type': 'application/json'}
    )
    
    lambda_response = response.json()
    return Response(
        lambda_response.get('body', ''),
        status=lambda_response.get('statusCode', 200),
        headers=lambda_response.get('headers', {})
    )

@app.route('/health')
def health():
    """Health check endpoint"""
    return {'status': 'healthy'}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
