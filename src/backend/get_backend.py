"""Module to get the appropriate reader based on configuration."""
from backend.local_backend import LocalBackend
from backend.aws_backend import AwsBackend

def get_backend(config):
    """Factory function to get the appropriate reader based on config."""
    reader_type = config.get('reader_type', 'local')

    if reader_type == 'local':
        return LocalBackend(config.get('base_path', ''))
    elif reader_type == 'remote':
        return AwsBackend(config.get('remote_url', ''))
    else:
        raise ValueError(f"Unknown reader type: {reader_type}")
