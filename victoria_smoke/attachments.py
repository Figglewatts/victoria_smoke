"""attachments.py

Attachments is responsible for building an index of attachment libraries.

Author:
    Sam Gibson <sgibson@glasswallsolutions.com>
"""
from __future__ import annotations
from collections import namedtuple
import logging
import os
from os import path
import random
from typing import List, Callable, Union

Attachment = namedtuple("Attachment", ["path", "size"])


class AttachmentLibrary:
    """AttachmentLibrary is used to load attachments and filter by various
    factors.

    Attributes:
        index (List[str]): The list of attachments in the library.
    """
    def __init__(self, libraries: List[str]) -> None:
        """Create an attachment library from a list of folders.

        Args:
            libraries (List[str]): The list of folders to use as libraries.
        """
        self.index: List[str] = []
        for library in libraries:
            if not path.exists(library):
                logging.warning(
                    f"library path '{library}' did not exist, skipping")
                continue
            self._index(library)

    @classmethod
    def from_attachments(cls,
                         attachments: List[Attachment]) -> AttachmentLibrary:
        """Create a new attachment library from a list of attachments.

        Args:
            files (List[Attachment]): A list of paths to files.

        Returns:
            AttachmentLibrary: The created attachment library.
        """
        self = cls.__new__(cls)
        self.index = attachments
        return self

    def _index(self, library: str) -> None:
        """Walk a single library directory and add it to the index.

        Args:
            library (str): The path to the library.
        """
        for dirpath, _, filenames in os.walk(library):
            for filename in filenames:
                full_path = path.join(dirpath, filename)
                file_size = path.getsize(full_path)
                self.index.append(Attachment(full_path, file_size))

    def filter_func(self, filter_func: Callable[[Attachment], bool]
                    ) -> AttachmentLibrary:
        """Filter the files in the index using a filtering function.

        Args:
            filter_func (Callable[[Attachment], bool]): The lambda to filter by.
                Accepts an attachment, and returns a bool indicating whether to
                include this attachment in the result or not.

        Returns:
            AttachmentLibrary: The library, filtered by the given function.
        """
        return AttachmentLibrary.from_attachments(
            [item for item in self.index if filter_func(item)])

    def get_filename(self, filename: str) -> AttachmentLibrary:
        """Filter the library for all attachments with a given filename.

        Args:
            filename (str): The filename to search for.

        Returns:
            AttachmentLibrary: The library, filtered by filename.
        """
        return self.filter_func(
            lambda item: path.basename(item.path) == filename)

    def get_like(self, search_term: str) -> AttachmentLibrary:
        """Filter the library for all attachments containing a search term.

        Args:
            search_term (str): The term to check for. Can be a full path if you want!

        Returns:
            AttachmentLibrary: The library, filtered by search term.
        """
        return self.filter_func(lambda item: search_term in item.path)

    def get_filetype(self, filetype: str) -> AttachmentLibrary:
        """Filter the library for all attachments with a file type.

        Args:
            filetype (str): The file type to filter by, i.e. 'pdf'.

        Returns:
            AttachmentLibrary: The library, filtered by filetype.
        """
        return self.filter_func(
            lambda item: path.splitext(item.path)[1][1:] == filetype)

    def get_directory(self, directory: str) -> AttachmentLibrary:
        """Filter the library for all attachments in a certain directory.

        Args:
            directory (str): The directory to filter by.

        Returns:
            AttachmentLibrary: The library, filtered by directory.
        """
        return self.filter_func(
            lambda item: directory in path.dirname(item.path).split(path.sep))

    def get_filesize(self, max_bytes: int,
                     min_bytes: int = 0) -> AttachmentLibrary:
        """Filter the library for all attachments within specified filesize 
        bounds.

        Args:
            max_bytes (int): The maximum bytes a file could have (inclusive).
            min_bytes (int): The minimum bytes a file could have (inclusive).

        Returns:
            AttachmentLibrary: The library, filtered by filesize.
        """
        return self.filter_func(
            lambda item: min_bytes <= item.size <= max_bytes)

    def random_choice(self, count: int,
                      seed: Union[int, None] = None) -> AttachmentLibrary:
        """Filter the library to a random choice of files.

        Args:
            count (int): The number of random files to pick.
            seed (int): The random seed to use, for determinism.
        
        Returns:
            AttachmentLibrary: The library, randomly chosen from.
        """
        random.seed(seed)
        return AttachmentLibrary.from_attachments(
            [item for item in random.sample(self.index, k=count)])
