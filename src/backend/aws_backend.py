""""AWS Backend Module."""
import logging
import boto3
from boto3.dynamodb.conditions import Key
from werkzeug.exceptions import NotFound, InternalServerError

from backend.backend import Backend
from config.app_config import AppConfig

logger = logging.getLogger(__name__)
boto3.set_stream_logger('boto3.resources', logging.INFO)
config = AppConfig()

class AwsBackend(Backend):
    """A reader that reads content from AWS S3 and DynamoDB."""
    def __init__(self):
        try:
            self.dynamodb = boto3.resource('dynamodb')
            self.s3 = boto3.client('s3')
            self.bucket_name = config.get('assets_bucket')
        except Exception as e:
            logger.error("Error initializing AWS resources: %s", e)
            raise InternalServerError("Failed to initialize AWS resources.") from e

    def get_post(self, slug):
        try: 
            table = self.dynamodb.Table('PostContent')
            response = table.query(KeyConditionExpression=Key('PostID').eq(slug))

            item = response.get('Items')
            if item:
                return {'slug': slug, **item[0]['Content']}
        except Exception as e:
            logger.error("Error fetching post '%s': %s", slug, e)
            raise InternalServerError(f"An error occurred while reading the post '{slug}'.") from e
        # If got here, no item found
        raise NotFound(f"Post with slug '{slug}' not found.")

    def get_content(self, content_uri):
        try:
            bucket = self.bucket_name
            key = content_uri.lstrip('/')

            response = self.s3.get_object(Bucket=bucket, Key=key)

            content = response['Body'].read()
            content = content.decode('utf-8')

            return content
        except self.s3.exceptions.NoSuchKey as e:
            logger.error("Content with URI '%s' not found: %s", content_uri, e)
            raise NotFound(f"Content with URI '{content_uri}' not found.") from e
        except Exception as e:
            logger.error("Error fetching content '%s': %s", content_uri, e)
            raise InternalServerError(
                f"An error occurred while reading the content '{content_uri}'.") from e

    def get_all_posts(self):
        try:
            table = self.dynamodb.Table('PostContent')
            response = table.scan()
            items = response.get('Items', [])

            for i, item in enumerate(items):
                if i > 0 and i % 10 == 0:  # Log progress every 10 items
                    yield {'slug': item['PostID'], **item['Content']}
        except Exception as e:
            logger.error("Error fetching all posts: %s", e)
            raise InternalServerError("An error occurred while reading the posts.") from e
