"""A simple local file reader that reads the content of a file from the local filesystem."""
from glob import glob
from typing import Generator
import logging

from yaml import load, SafeLoader
from werkzeug.exceptions import NotFound, InternalServerError

from backend.backend import Backend
from models import Post

logger = logging.getLogger(__name__)

class LocalBackend(Backend):
    """A reader that reads content from a local file."""
    def __init__(self, base_path):
        self.base_path = base_path

    def get_post(self, slug: str) -> Post:
        """Read the content of a local file based on the slug."""
        try:
            file_path = f"{self.base_path}{slug}.yml"
            with open(file_path, 'r', encoding='utf-8') as file:
                content = load(file, Loader=SafeLoader)
                content['slug'] = slug
                return Post(**content)
        except FileNotFoundError as exc:
            logger.error("Post with slug '%s' not found: %s", slug, exc)
            raise NotFound(f"Post with slug '{slug}' not found.") from exc
        except Exception as exc:
            logger.error("Error reading post '%s': %s", slug, exc)
            raise InternalServerError(
                f"An error occurred while reading the post '{slug}'.") from exc

    def get_content(self, content_uri: str) -> str:
        """Read the content of a local file based on the relative path."""
        try:
            with open(content_uri, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError as exc:
            logger.error("Content with URI '%s' not found: %s", content_uri, exc)
            raise NotFound(f"Content with URI '{content_uri}' not found.") from exc
        except Exception as exc:
            logger.error("Error reading content '%s': %s", content_uri, exc)
            raise InternalServerError(
                f"An error occurred while reading the content '{content_uri}'.") from exc


    def get_all_posts(self) -> Generator[Post, None, None]:
        """Fetch data for the index view."""
        try:
            index_files = glob(f"{self.base_path}/*.yml")
            for file_path in index_files:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = load(file, Loader=SafeLoader)
                    content['slug'] = file_path.split('/')[-1].replace('.yml', '')
                    yield Post(**content)
        except FileNotFoundError as exc:
            logger.error("No posts found: %s", exc)
            raise NotFound("No posts found.") from exc
        except Exception as exc:
            logger.error("Error reading posts: %s", exc)
            raise InternalServerError(
                "An error occurred while reading the posts.") from exc
