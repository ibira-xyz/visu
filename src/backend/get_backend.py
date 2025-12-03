"""Module to get the appropriate reader based on configuration."""
from backend.local_backend import LocalBackend
from backend.aws_backend import AwsBackend
from config import AppConfig

config = AppConfig()

def get_backend():
    """Factory function to get the appropriate reader based on config."""
    backend_type = config.get('backend_type', 'local')

    if backend_type == 'local':
        return LocalBackend(config.get('base_path', ''))
    elif backend_type == 'aws':
        return AwsBackend()
    else:
        raise ValueError(f"Unknown backend type: {backend_type}")