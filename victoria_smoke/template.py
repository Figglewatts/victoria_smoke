from datetime import datetime
import functools
import random
import types
from typing import List, Union, Iterable
import uuid

from faker import Faker
from faker.providers import BaseProvider
from jinja2 import Template, Environment, FunctionLoader

from .attachments import AttachmentLibrary
from .faker_text_provider import TextProvider
from . import util


def create_environment() -> Environment:
    """Create the Jinja environment containing the functionality to render
    templates."""
    env = Environment()

    # define the filterfunc decorator and patch it into the environment
    # so we can define filters using a decorator
    def filterfunc(target, func):
        target.filters[func.__name__] = func

    env.filterfunc = types.MethodType(filterfunc, env)

    return env


# The template environment used to render the templates
template_env = create_environment()


def _emit_yaml_array(strs: List[str]) -> str:
    """Take a list of strings and convert them into YAML array format."""
    return "\n".join([f"- {s}" for s in strs])


@template_env.filterfunc
def to_array(library) -> str:
    """Convert an Attachment library to a YAML array."""
    if type(library) != AttachmentLibrary:
        raise TypeError(
            f"Cannot use 'to_array' filter with type '{type(library).__name__}'"
        )
    return _emit_yaml_array([item.path for item in library.index])


@template_env.filterfunc
def collapse(iterable: Iterable, join="\n  ") -> str:
    """Collapse an iterable to a single string."""
    return join.join(iterable)


@template_env.filterfunc
def to_ascii(byte_arr) -> str:
    """Convert bytes into an ASCII str."""
    return bytes([b % 128 for b in byte_arr]).decode("ascii")


@template_env.filterfunc
def filename(library, filename: str) -> AttachmentLibrary:
    """Filter an attachment library by filename."""
    if type(library) != AttachmentLibrary:
        raise TypeError(
            f"Cannot use 'filename' filter with type '{type(library).__name__}'"
        )

    return library.get_filename(filename)


@template_env.filterfunc
def like(library, search_term: str) -> AttachmentLibrary:
    """Filter an attachment library by search term."""
    if type(library) != AttachmentLibrary:
        raise TypeError(
            f"Cannot use 'like' filter with type '{type(library).__name__}'")

    return library.get_like(search_term)


@template_env.filterfunc
def filetype(library, filetype: str) -> AttachmentLibrary:
    """Filter an attachment library by file type."""
    if type(library) != AttachmentLibrary:
        raise TypeError(
            f"Cannot use 'filetype' filter with type '{type(library).__name__}'"
        )

    return library.get_filetype(filetype)


@template_env.filterfunc
def directory(library, directory: str) -> AttachmentLibrary:
    """Filter an attachment library by directory."""
    if type(library) != AttachmentLibrary:
        raise TypeError(
            f"Cannot use 'directory' filter with type '{type(library).__name__}'"
        )

    return library.get_directory(directory)


@template_env.filterfunc
def filesize(library, maximum: str = "0", minimum: str = "0") -> AttachmentLibrary:
    """Filter an attachment library by file size."""
    if type(library) != AttachmentLibrary:
        raise TypeError(
            f"Cannot use 'filesize' filter with type '{type(library).__name__}'"
        )

    max_bytes = util.filesize_str_to_bytes(maximum)
    min_bytes = util.filesize_str_to_bytes(minimum)

    return library.get_filesize(max_bytes=max_bytes, min_bytes=min_bytes)


@template_env.filterfunc
def randomly_pick(library, count: int,
                  seed: Union[int, None] = None) -> AttachmentLibrary:
    """Choose an amount of items from the library at random."""
    if type(library) != AttachmentLibrary:
        raise TypeError(
            f"Cannot use 'randomly_pick' filter with type '{type(library).__name__}'"
        )

    return library.random_choice(count=count, seed=seed)


def process(email_template: str, attachment_library: AttachmentLibrary) -> str:
    template = template_env.from_string(email_template)
    fake = Faker()
    fake.add_provider(TextProvider)
    return template.render(library=attachment_library,
                           fake=fake,
                           datetime=datetime,
                           uuid=uuid)
