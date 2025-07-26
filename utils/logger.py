# Shared logger utility
import logging

LOG_FORMAT = '%(asctime)s | %(levelname)s | %(name)s | %(message)s'
LOG_LEVEL = logging.INFO

logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)

def get_logger(name: str = __name__):
    """Get a logger with the specified name, pre-configured for the app."""
    return logging.getLogger(name) 