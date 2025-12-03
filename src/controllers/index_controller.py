"""Controller for index view logic."""
import logging
import time
from config import AppConfig

logger = logging.getLogger(__name__)
app_config = AppConfig()

class IndexController:
    """Controller for handling index view logic."""
    def _process_post(self, post):
        """Process a single post item."""
        # Example processing logic; can be customized as needed
        result = {
            "title": post.get("title"),
            "description": post.get("description"),
            "banner": post.get("banner"),
            "link": app_config.get("base_url") + 'post/' + post.get("slug")
        }
        return result

    def run(self, index_data):
        """Fetch data for the index view."""
        process_start = time.time()
        logger.info("IndexController starting to process %d posts", len(index_data))

        # Fetch and return data needed for the index view
        processed_data = []
        for i, item in enumerate(index_data):
            if i > 0 and i % 5 == 0:  # Log progress every 5 items
                logger.info("Processed %d/%d posts", i, len(index_data))
            processed_data.append(self._process_post(item))

        process_time = time.time() - process_start
        logger.info(
            "IndexController completed processing %d posts in %.3f seconds",
            len(processed_data), process_time)

        return {"items": processed_data}
