"""Controller for index view logic."""
import logging
import time
from config import AppConfig
from models import Post

logger = logging.getLogger(__name__)
app_config = AppConfig()


def process_posts(index_data: list[Post]) -> dict:
    """Fetch data for the index view."""
    process_start = time.time()
    logger.info("IndexController starting to process posts")

    # Fetch and return data needed for the index view
    processed_data = []
    for i, item in enumerate(index_data):
        if i > 0 and i % 5 == 0:  # Log progress every 5 items
            logger.info("Processed %d/%d posts", i, len(index_data))
        processed_data.append(item)

    process_time = time.time() - process_start
    logger.info(
        "IndexController completed processing %d posts in %.3f seconds",
        len(processed_data), process_time)

    return {"context": processed_data}
