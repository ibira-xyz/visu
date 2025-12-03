"""Controller for index view logic."""
from config import AppConfig

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
        # Fetch and return data needed for the index view
        processed_data = [self._process_post(item) for item in index_data]
            
        return {"items": processed_data}