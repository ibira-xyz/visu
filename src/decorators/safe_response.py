""""Decorator to handle exceptions and return safe HTTP responses"""
from traceback import format_exc

from functools import wraps
from werkzeug.exceptions import NotFound, InternalServerError

from views.not_found import render_not_found
from views.server_error import render_server_error
from loggers import get_logger

logger = get_logger(__name__)

def safe_response(func):
    """Decorator to handle exceptions and return safe HTTP responses"""
    @wraps(func)
    def wrapper(**args):
        try:
            return func(**args)
        except NotFound:
            msg = format_exc()
            logger.warning(msg)
            return {
                'statusCode': 404,
                'headers': {
                    'Content-Type': 'text/html'
                },
                'body': render_not_found()
            }
        except InternalServerError:
            msg = format_exc()
            logger.error(msg)
            return {
                'statusCode': 500,
                'headers': {
                    'Content-Type': 'text/html'
                },
                'body': render_server_error()
            }
        except Exception: #pylint: disable=broad-except
            msg = format_exc()
            logger.critical(msg)
            return {
                'statusCode': 500,
                'headers': {
                    'Content-Type': 'text/html'
                },
                'body': render_server_error()
            }
    return wrapper