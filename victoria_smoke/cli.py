"""cli.py

This is the module that contains the Click CLI for the plugin.

Author:
    Sam Gibson <sgibson@glasswallsolutions.com>
"""
import logging

import click

from .attachments import AttachmentLibrary
from .config import SmokeConfig
from . import spec as spc
from . import template as tmpl


@click.group()
@click.pass_obj
def smoke(cfg: SmokeConfig):
    """Perform smoke tests on clusters."""
    pass


@smoke.command()
@click.argument("spec", nargs=1, required=True, type=str)
@click.option("--output-file",
              "-o",
              help="The file to output the spec to.",
              metavar="FILE")
@click.pass_obj
def template(cfg: SmokeConfig, spec: str, output_file: str):
    """Template a spec file."""
    attachments = AttachmentLibrary(cfg.attachment_libraries)
    with open(spec, "r") as spec_file:
        templated_spec = tmpl.process(spec_file.read(), attachments)
        if output_file is None:
            logging.info(templated_spec)
        else:
            with open(output_file, "w") as output_file_handle:
                output_file_handle.write(templated_spec)
            logging.info(f"Templated '{spec}' to file '{output_file}'")


@smoke.command()
@click.argument("spec", nargs=1, required=True, type=str)
@click.option("--output-file",
              "-o",
              help="The file to render the spec to.",
              metavar="FILE")
@click.pass_obj
def render(cfg: SmokeConfig, spec: str, output_file: str):
    """Render a spec to MIME."""
    attachments = AttachmentLibrary(cfg.attachment_libraries)
    with open(spec, "r") as spec_file:
        loaded_spec = spc.from_yaml(spec_file.read(), attachments)
        mime_str = loaded_spec.as_mime().as_string()
        if output_file is None:
            logging.info(mime_str)
        else:
            with open(output_file, "w") as output_file_handle:
                output_file_handle.write(mime_str)
            logging.info(f"Rendered '{spec}' to file '{output_file}'")


@smoke.command()
@click.argument("cluster", nargs=-1, required=True)
@click.pass_obj
def test(cfg: SmokeConfig):
    """Perform a smoke test on a cluster."""
    pass