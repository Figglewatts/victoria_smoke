import builtins
from collections import namedtuple
import contextlib
import io
import os
import os.path

import pytest

from victoria_smoke.attachments import AttachmentLibrary, Attachment
from victoria_smoke import util

test_files = [
    f".{os.sep}root_file_1.txt", f".{os.sep}root_file_2.txt",
    f"subdir{os.sep}subfile_1.txt", f"subdir{os.sep}subfile_2.txt",
    f".{os.sep}pdf_file.pdf", f".{os.sep}big_file.txt"
]

test_files_dirs = [f".{os.sep}", f"subdir{os.sep}"]


@pytest.fixture
def mock_open(monkeypatch):
    """Fixture used to mock open() to make sure tests don't write to the
    host filesystem."""
    files = {}

    @contextlib.contextmanager
    def mocked_open(filename, *args, **kwargs):
        file = io.StringIO(files.get(filename, ""))
        try:
            yield file
        finally:
            files[filename] = file.getvalue()
            file.close()

    monkeypatch.setattr(builtins, "open", mocked_open)


@pytest.fixture
def mock_attachment_library(mock_open):
    for f in test_files:
        with open(f, 'w') as attachment_file:
            if f == "big_file.txt":
                attachment_file.write("MUCH LONGER FILE!!!!!!!!!!!")
            else:
                attachment_file.write("Regular file")


@pytest.fixture
def mock_os_funcs(monkeypatch):
    class MockDirEntry:
        def __init__(self, path, size):
            self.path = path
            self.sz = size

        def stat(self):
            return namedtuple("stat_result", ["st_size"])(self.sz)

        def is_file(self):
            return True

    def mock_scantree(*args, **kwargs):
        for test_file in test_files:
            yield MockDirEntry(test_file, mock_getsize(test_file))

    def mock_getsize(*args, **kwargs):
        if args[0] == f".{os.sep}big_file.txt":
            return 2000
        else:
            return 1000

    def mock_exists(path):
        return True

    monkeypatch.setattr(util, "scantree", mock_scantree)
    monkeypatch.setattr(os.path, "exists", mock_exists)


@pytest.fixture
def library(mock_open, mock_os_funcs):
    return AttachmentLibrary([""])


def get_filenames(library: AttachmentLibrary):
    return [attachment.path for attachment in library.index]


def test_create_library(library):
    assert library.index == [
        Attachment(os.path.normpath(f".{os.sep}root_file_1.txt"), 1000),
        Attachment(os.path.normpath(f".{os.sep}root_file_2.txt"), 1000),
        Attachment(os.path.normpath(f"subdir{os.sep}subfile_1.txt"), 1000),
        Attachment(os.path.normpath(f"subdir{os.sep}subfile_2.txt"), 1000),
        Attachment(os.path.normpath(f".{os.sep}pdf_file.pdf"), 1000),
        Attachment(os.path.normpath(f".{os.sep}big_file.txt"), 2000)
    ]


def test_get_filename(library):
    files = library.get_filename("root_file_1.txt")
    assert get_filenames(files) == [
        os.path.normpath(f".{os.sep}root_file_1.txt")
    ]


def test_get_like(library):
    files = library.get_like("subfile")
    assert get_filenames(files) == [
        os.path.normpath(f"subdir{os.sep}subfile_1.txt"),
        os.path.normpath(f"subdir{os.sep}subfile_2.txt")
    ]


def test_get_extension(library):
    files = library.get_filetype("pdf")
    assert get_filenames(files) == [os.path.normpath(f".{os.sep}pdf_file.pdf")]


def test_get_directory(library):
    files = library.get_directory("subdir")
    assert get_filenames(files) == [
        os.path.normpath(f"subdir{os.sep}subfile_1.txt"),
        os.path.normpath(f"subdir{os.sep}subfile_2.txt")
    ]


@pytest.mark.parametrize("min_bytes,max_bytes,expected",
                         [(0, 0, len(test_files)), (1500, 0, 1),
                          (0, 1500, len(test_files) - 1),
                          (500, 2500, len(test_files))])
def test_get_filesize(library, min_bytes, max_bytes, expected):
    files = library.get_filesize(min_bytes=min_bytes, max_bytes=max_bytes)
    assert len(get_filenames(files)) == expected


def test_random_choice(library):
    # seed is important here, as without it the test is nondeterministic
    files = library.random_choice(count=2, seed=1337)
    assert get_filenames(files) == [
        os.path.normpath(f".{os.sep}pdf_file.pdf"),
        os.path.normpath(f".{os.sep}big_file.txt")
    ]