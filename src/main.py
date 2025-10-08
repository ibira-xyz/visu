import os
from flask import Flask, render_template

app = Flask(__name__)

# Detect if running in Docker
CDN_BASE_URL = os.environ.get('CDN_BASE_URL')

@app.context_processor
def inject_static_url():
    def static_url(filename):
        url = f"static/{filename}"
        if CDN_BASE_URL:
            url = f"{CDN_BASE_URL}/{url}"
        return url
    return dict(static_url=static_url)

@app.route("/")
def home():
    return render_template("index.html")

# Lambda handler function
def lambda_handler(*_):
    """AWS Lambda handler function"""
    with app.app_context():
        html_content = home()
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/html'
            },
            'body': html_content
        }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
