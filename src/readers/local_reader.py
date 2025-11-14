"""A simple local file reader that reads the content of a file from the local filesystem."""

from readers.reader import Reader


class LocalReader(Reader):
    """A reader that reads content from a local file."""
    def __init__(self, file_path):
        self.file_path = file_path

    def read(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            return file.read()
