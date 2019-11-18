"""setup.py

Used for installing victoria_smoke via pip.

Author:
    Sam Gibson <sgibson@glasswallsolutions.com>
"""
from setuptools import setup, find_packages

setup(
    dependency_links=[],
    install_requires=["victoria", "click", "marshmallow"],
    name="victoria_smoke",
    version="0.1.0",
    description="Victoria plugin to perform smoke tests",
    author="Sam Gibson",
    author_email="sgibson@glasswallsolutions.com",
    packages=find_packages(),
)