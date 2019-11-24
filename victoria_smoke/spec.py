from datetime import datetime
from email import message
from email.mime.text import MIMEText
from typing import List

from marshmallow import Schema, fields, post_load, INCLUDE
from sremail.message import MessageHeadersSchema, Message, MESSAGE_HEADERS_SCHEMA
import yaml

from .attachments import AttachmentLibrary
from . import template


class SpecSchema(Schema):
    headers = fields.Dict(keys=fields.Str(), values=fields.Raw())
    body = fields.Str(required=True)
    attach = fields.List(fields.Str(), required=True)

    @post_load
    def make_spec(self, data, **kwargs):
        return Spec(**data)


SPEC_SCHEMA = SpecSchema()


class Spec:
    def __init__(self, headers: dict, body: str, attach: List[str]) -> None:
        self.headers = MESSAGE_HEADERS_SCHEMA.load(headers)
        self.body = body
        self.attach = attach

    def as_message(self) -> Message:
        msg = Message(**self.headers)
        for attachment in self.attach:
            msg.attach(attachment)
        return msg

    def as_mime(self) -> message.Message:
        msg = self.as_message()
        mime = msg.as_mime()
        body_part = MIMEText(self.body, "plain")
        mime.attach(body_part)
        mime["Date"] = datetime.fromisoformat(
            mime["Date"]).strftime("%a, %d %b %Y %H:%M:%S %z")
        return mime


def from_yaml(spec_yaml: str, attachment_library: AttachmentLibrary) -> Spec:
    templated_yaml = template.process(spec_yaml, attachment_library)
    raw_spec = yaml.safe_load(templated_yaml)
    return SPEC_SCHEMA.load(raw_spec)