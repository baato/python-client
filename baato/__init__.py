import logging
from logging import NullHandler
from baato.main import BaatoClient

__all__ = ("BaatoClient",)

# Set default logging handler to avoid "No handler found" warnings.
logging.getLogger(__name__).addHandler(NullHandler())
