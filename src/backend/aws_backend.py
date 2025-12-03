""""AWS Backend Module."""
import boto3
from boto3.dynamodb.conditions import Key

from backend.backend import Backend
from config.app_config import AppConfig

config = AppConfig()

class AwsBackend(Backend):
    """A reader that reads content from AWS S3 and DynamoDB."""
    def __init__(self, remote_url):
        self.remote_url = remote_url
        self.dynamodb = boto3.resource('dynamodb')
        self.s3 = boto3.client('s3')

        self.bucket_name = config.get('assets_bucket')

    def get_post(self, slug):
        table = self.dynamodb.Table('PostContent')
        response = table.query(KeyConditionExpression=Key('PostID').eq(slug))
        item = response.get('Items')
        if item:
            return {'slug': slug, **item[0]['Content']}
        else:
            return None

    def get_content(self, content_uri):
        bucket = self.bucket_name
        key = content_uri.lstrip('/')
        response = self.s3.get_object(Bucket=bucket, Key=key)
        content = response['Body'].read()
        content = content.decode('utf-8')
        return content

    def fetch_index_data(self):
        table = self.dynamodb.Table('PostContent')
        response = table.scan()
        items = response.get('Items', [])
        for item in items:
            yield {'slug': item['PostID'], **item['Content']}
