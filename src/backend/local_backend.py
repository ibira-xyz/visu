"""A simple local file reader that reads the content of a file from the local filesystem."""
from glob import glob

from yaml import load, SafeLoader

from backend.backend import Backend


class LocalBackend(Backend):
    """A reader that reads content from a local file."""
    def __init__(self, base_path):
        self.base_path = base_path

    def get_post(self, slug):
        """Read the content of a local file based on the slug."""
        file_path = f"{self.base_path}{slug}.yml"
        with open(file_path, 'r', encoding='utf-8') as file:
            content = load(file, Loader=SafeLoader)
            content['slug'] = slug
            return content

    def get_content(self, content_uri):
        """Read the content of a local file based on the relative path."""
        with open(content_uri, 'r', encoding='utf-8') as file:
            return file.read()

    def get_all_posts(self):
        """Fetch data for the index view."""
        index_files = glob(f"{self.base_path}/*.yml")
        for file_path in index_files:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = load(file, Loader=SafeLoader)
                content['slug'] = file_path.split('/')[-1].replace('.yml', '')
                yield content