"""cli.py

This is the module that contains the Click CLI for the plugin.

Author:
    Sam Gibson <sgibson@glasswallsolutions.com>
"""
import click

from .config import SmokeConfig
from .template import process

TMPL = """{{ library | filesize(maximum="1.5kb") | like("cli") | to_array }}
{{ fake.texts(10) | collapse }}"""


@click.command()
@click.pass_obj
@click.argument("cluster", nargs=-1, required=True)
def smoke(cfg: SmokeConfig, cluster):
    """Perform smoke tests on clusters."""
    process(TMPL)
