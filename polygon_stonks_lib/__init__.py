"""
Polygon Stonks - A Python library for analyzing gapped stocks using Polygon.io API.
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .gap_analyzer import GapAnalyzer
from .utils import calculate_overnight_change

__all__ = ["GapAnalyzer", "calculate_overnight_change"]
