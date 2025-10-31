"""Content sourcing module for fetching interesting facts"""

from .fetchers import FactFetcher
from .parsers import FactParser

__all__ = ['FactFetcher', 'FactParser']
