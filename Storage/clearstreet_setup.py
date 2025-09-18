"""
Setup script for clearstreet_trading_lib package.
"""

from setuptools import setup, find_packages

# Read requirements
with open("clearstreet_trading_lib/requirements.txt", "r") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="clearstreet_trading_lib",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Python library for interacting with ClearStreet Trading API",
    long_description="A comprehensive Python library for ClearStreet Trading API integration with OAuth2 authentication, account management, order placement, and market data retrieval.",
    long_description_content_type="text/plain",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.900",
        ],
    },
)
