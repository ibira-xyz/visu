"""AWS Lambda handler for the home route"""
import logging
import time
from backend import get_backend
from controllers import index_controller
from views import render_index
from responses import safe_response, lambda_response

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

logger.info("Lambda handler starting - initializing components")
start_time = time.time()

backend = get_backend()
logger.info("Backend initialized in %.3f seconds", time.time() - start_time)
logger.info("All components initialized in %.3f seconds", time.time() - start_time)


@safe_response(lambda_response)
def handler(_event, _context):
    """AWS Lambda handler function"""
    handler_start = time.time()
    logger.info("Handler execution started")

    # Step 1: Fetch index data
    fetch_start = time.time()
    logger.info("Starting to fetch index data from backend")

    # Monitor fetch progress with periodic updates
    index_data = []
    data_generator = backend.get_all_posts()

    for i, item in enumerate(data_generator):
        if time.time() - fetch_start > 8.0:  # If taking more than 8 seconds
            logger.warning("Fetch operation taking too long (>8s), stopping at %d items", i)
            break
        index_data.append(item)
        if i > 0 and i % 5 == 0:
            elapsed = time.time() - fetch_start
            logger.info("Fetched %d items in %.3f seconds", i + 1, elapsed)

    fetch_time = time.time() - fetch_start
    logger.info("Index data fetched in %.3f seconds. Found %d items",
                fetch_time, len(index_data))

    # Step 2: Process data through controller
    controller_start = time.time()
    logger.info("Starting controller processing")

    controller_result = index_controller.process_posts(index_data)
    controller_time = time.time() - controller_start
    logger.info("Controller processing completed in %.3f seconds", controller_time)

    # Step 3: Render view
    render_start = time.time()
    logger.info("Starting view rendering")

    html_content = render_index(**controller_result)
    render_time = time.time() - render_start
    logger.info("View rendering completed in %.3f seconds", render_time)

    total_time = time.time() - handler_start
    logger.info("Handler execution completed successfully in %.3f seconds", total_time)

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/html'
        },
        'body': html_content
    }
