"""victoria_smoke

A Victoria plugin to perform smoke tests.

Author:
    Sam Gibson <sgibson@glasswallsolutions.com>
"""
from victoria.plugin import Plugin

from .config import SmokeConfigSchema
from . import cli

plugin = Plugin(name="smoke", cli=cli.smoke, config_schema=SmokeConfigSchema())