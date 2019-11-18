"""attachments.py

Attachments is responsible for building an index of attachment libraries.

Author:
    Sam Gibson <sgibson@glasswallsolutions.com>
"""
from collections import namedtuple
import os
from os import path
from typing import List, Callable

Attachment = namedtuple("Attachment", ["path", "size"])


class AttachmentLibrary:
    def __init__(self, libraries: List[str]) -> None:
        self.index: List[str] = []
        for library in libraries:
            self._index(library)

    def _index(self, library: str) -> None:
        for dirpath, _, filenames in os.walk(library):
            for filename in filenames:
                full_path = path.join(dirpath, filename)
                file_size = path.getsize(full_path)
                self.index.append(Attachment(full_path, file_size))

    def filter_func(self, filter_func: Callable[[str], bool]) -> List[str]:
        return [item for item in self.index if filter_func(item)]

    def get_filename(self, filename: str) -> List[str]:
        return self.filter_func(lambda item: path.basename(item) == filename)

    def get_like(self, search_term: str) -> List[str]:
        return self.filter_func(lambda item: search_term in item)

    def get_extension(self, extension: str) -> List[str]:
        return self.filter_func(
            lambda item: path.splitext(item)[1][1:] == extension)

    def get_directory(self, directory: str) -> List[str]:
        return self.filter_func(
            lambda item: directory in path.dirname(item).split(path.sep))
