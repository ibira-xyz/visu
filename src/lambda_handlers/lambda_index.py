"""AWS Lambda handler for the home route"""
import logging
import time
from backend import get_backend
from controllers import IndexController, PostController
from views import IndexView, PostView

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

logger.info("Lambda handler starting - initializing components")
start_time = time.time()

backend = get_backend()
logger.info("Backend initialized in %.3f seconds", time.time() - start_time)

index_controller = IndexController()
logger.info("IndexController initialized in %.3f seconds", time.time() - start_time)

index_view = IndexView()
logger.info("IndexView initialized in %.3f seconds", time.time() - start_time)

post_controller = PostController(backend)
post_view = PostView()
logger.info("All components initialized in %.3f seconds", time.time() - start_time)


def handler(_event, _context):
    """AWS Lambda handler function"""
    handler_start = time.time()
    logger.info("Handler execution started")

    try:
        # Step 1: Fetch index data
        fetch_start = time.time()
        logger.info("Starting to fetch index data from backend")

        # Monitor fetch progress with periodic updates
        index_data = []
        data_generator = backend.fetch_index_data()

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

        controller_result = index_controller.run(index_data)
        controller_time = time.time() - controller_start
        logger.info("Controller processing completed in %.3f seconds", controller_time)

        # Step 3: Render view
        render_start = time.time()
        logger.info("Starting view rendering")

        html_content = index_view.render(**controller_result)
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

    except Exception as e:  # pylint: disable=broad-except
        error_time = time.time() - handler_start
        logger.error("Handler failed after %.3f seconds with error: %s", error_time, str(e))
        logger.exception("Full exception details:")

        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'text/html'
            },
            'body': "<html><body><h1>Internal Server Error</h1><p>" + str(e) + "</p></body></html>"
        }
