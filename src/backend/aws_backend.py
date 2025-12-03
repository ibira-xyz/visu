""""AWS Backend Module."""
import logging
import time
import boto3
from boto3.dynamodb.conditions import Key

from backend.backend import Backend
from config.app_config import AppConfig

logger = logging.getLogger(__name__)
boto3.set_stream_logger('boto3.resources', logging.INFO)
config = AppConfig()

class AwsBackend(Backend):
    """A reader that reads content from AWS S3 and DynamoDB."""
    def __init__(self):
        init_start = time.time()
        logger.info("Initializing AwsBackend")

        logger.info("Creating DynamoDB resource")
        self.dynamodb = boto3.resource('dynamodb')

        logger.info("Creating S3 client")
        self.s3 = boto3.client('s3')

        self.bucket_name = config.get('assets_bucket')
        logger.info("AwsBackend initialized in %.3f seconds", time.time() - init_start)

    def get_post(self, slug):
        query_start = time.time()
        logger.info("Querying DynamoDB for post: %s", slug)

        table = self.dynamodb.Table('PostContent')
        response = table.query(KeyConditionExpression=Key('PostID').eq(slug))

        query_time = time.time() - query_start
        logger.info("DynamoDB query completed in %.3f seconds", query_time)

        item = response.get('Items')
        if item:
            logger.info("Post found: %s", slug)
            return {'slug': slug, **item[0]['Content']}
        else:
            logger.warning("Post not found: %s", slug)
            return None

    def get_content(self, content_uri):
        s3_start = time.time()
        logger.info("Fetching content from S3: %s", content_uri)

        bucket = self.bucket_name
        key = content_uri.lstrip('/')

        logger.info("S3 get_object - Bucket: %s, Key: %s", bucket, key)
        response = self.s3.get_object(Bucket=bucket, Key=key)

        read_start = time.time()
        content = response['Body'].read()
        content = content.decode('utf-8')

        total_time = time.time() - s3_start
        read_time = time.time() - read_start
        logger.info("S3 content fetched in %.3f seconds (read: %.3f seconds)",
                    total_time, read_time)

        return content

    def fetch_index_data(self):
        scan_start = time.time()
        logger.info("Starting DynamoDB table scan for index data")

        table = self.dynamodb.Table('PostContent')
        response = table.scan()

        scan_time = time.time() - scan_start
        items = response.get('Items', [])
        logger.info("DynamoDB scan completed in %.3f seconds. Found %d items",
                    scan_time, len(items))

        process_start = time.time()
        for i, item in enumerate(items):
            if i > 0 and i % 10 == 0:  # Log progress every 10 items
                logger.info("Processed %d/%d items", i, len(items))
            yield {'slug': item['PostID'], **item['Content']}

        process_time = time.time() - process_start
        logger.info("All %d items processed in %.3f seconds", len(items), process_time)
