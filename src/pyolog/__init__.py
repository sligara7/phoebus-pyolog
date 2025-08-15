"""
Phoebus PyOlog - Python client for Phoebus Olog logbook service.

This package provides a Python client for interacting with the Phoebus Olog
logbook service, part of the Phoebus control system framework.
"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("phoebus-pyolog")
except PackageNotFoundError:
    # package is not installed
    __version__ = "unknown"

from .client import OlogClient

__all__ = ["OlogClient", "__version__"]
