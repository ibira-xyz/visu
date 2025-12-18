""""Decorator to handle exceptions and return safe HTTP responses"""
from traceback import format_exc
import logging

from functools import wraps
from werkzeug.exceptions import NotFound, InternalServerError
from boto3 import set_stream_logger

from views.not_found import render_not_found
from views.server_error import render_server_error

logging.basicConfig(level=logging.INFO)
set_stream_logger('boto3', logging.INFO)

def safe_response(response):
    """Decorator to handle exceptions and return safe HTTP responses"""
    def safe_response_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger = logging.getLogger(func.__name__)
            try:
                return func(*args, **kwargs)
            except NotFound:
                msg = format_exc()
                logger.warning(msg)
                return response(render_not_found(), 404)
            except InternalServerError:
                msg = format_exc()
                logger.error(msg)
                return response(render_server_error(), 500)
            except Exception: #pylint: disable=broad-except
                msg = format_exc()
                logger.critical(msg)
                return response(render_server_error(), 500)
        return wrapper
    return safe_response_decorator