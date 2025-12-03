"""Application configuration loader."""
import os
from dotenv import load_dotenv
from yaml import load, SafeLoader

class AppConfig:
    """Application configuration loader."""
    def __init__(self, config_path: str = None):
        load_dotenv()
        config_path = config_path or os.getenv("IBIRA_PATH")
        if not config_path:
            raise ValueError(
                "Configuration path must be provided via argument \
or IBIRA_PATH environment variable.")
        with open(config_path, "r", encoding="utf-8") as f:
            self.config = load(f, Loader=SafeLoader)

    def get(self, key: str, default=None):
        """Get a configuration value by key."""
        return self.config.get(key, default)
