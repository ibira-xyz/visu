"""Module to get the appropriate reader based on configuration."""
from drivers.local_driver import LocalDriver
from drivers.aws_driver import AwsDriver
from drivers.driver import Driver
from config import AppConfig

config = AppConfig()

def get_driver() -> Driver:
    """Factory function to get the appropriate reader based on config."""
    driver_type = config.get('driver_type', 'local')

    if driver_type == 'local':
        return LocalDriver(config.get('base_path', ''))
    if driver_type == 'aws':
        return AwsDriver()
    raise ValueError(f"Unknown driver type: {driver_type}")