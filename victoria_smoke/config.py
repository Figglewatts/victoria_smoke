"""config.py

Config defines the config used for the smoke testing plugin and a marshmallow
schema for validating the config.

Author:
    Sam Gibson <sgibson@glasswallsolutions.com>
"""
from typing import List

from marshmallow import Schema, fields, post_load


class SmokeConfigSchema(Schema):
    """Marshmallow schema for the smoke test plugin config."""
    attachment_libraries = fields.List(fields.Str(), required=True)

    @post_load
    def make_smoke_config(self, data, **kwargs):
        return SmokeConfig(**data)


class SmokeConfig:
    """SmokeConfig is the config for the smoke testing plugin."""
    def __init__(self, attachment_libraries: List[str]) -> None:
        self.attachment_libraries = attachment_libraries