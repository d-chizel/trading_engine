"""
Setup script for polygon_stonks package.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="polygon_stonks",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Python library for analyzing gapped stocks using Polygon.io API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/d-chizel/polygon_stonks",
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
    install_requires=[
        "pandas>=1.3.0",
        "polygon-api-client>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.900",
        ],
    },
    entry_points={
        "console_scripts": [
            "polygon-stonks=polygon_stonks.cli:main",
        ],
    },
)
