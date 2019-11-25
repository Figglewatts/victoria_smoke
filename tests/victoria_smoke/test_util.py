from contextlib import nullcontext as does_not_raise
import os

import pytest

from victoria_smoke import util


@pytest.mark.parametrize("value,expected,raises",
                         [("1", 1, does_not_raise()),
                          ("1b", 1, does_not_raise()),
                          ("5KB", 5000, does_not_raise()),
                          ("5     KB", 5000, does_not_raise()),
                          ("5kB", 5000, does_not_raise()),
                          ("1kib", 1024, does_not_raise()),
                          ("1ki", 1024, does_not_raise()),
                          ("5k", 5000, does_not_raise()),
                          ("5.5k", 5500, does_not_raise()),
                          ("5..5k", None, pytest.raises(ValueError)),
                          ("abc123", None, pytest.raises(ValueError)),
                          ("5hb", None, pytest.raises(ValueError))])
def test_filesize_str_to_bytes(value, expected, raises):
    with raises:
        result = util.filesize_str_to_bytes(value)
        assert result == expected


def test_scantree(monkeypatch):
    class MockDirEntry:
        def __init__(self, path, file):
            self.path = path
            self.file = file

        def is_dir(self, *args, **kwargs):
            return not self.file

    def mock_scandir(directory, *args, **kwargs):
        for entry in {
                "dir_a": [
                    MockDirEntry("dir_a/file_a.txt", True),
                    MockDirEntry("dir_a/file_b.txt", True),
                    MockDirEntry("dir_a/dir_b", False)
                ],
                "dir_a/dir_b": [MockDirEntry("dir_a/dir_b/file_c.txt", True)]
        }[directory]:
            yield entry

    monkeypatch.setattr(util, "scandir", mock_scandir)

    files = [entry.path for entry in util.scantree("dir_a")]
    assert files == [
        "dir_a/file_a.txt", "dir_a/file_b.txt", "dir_a/dir_b/file_c.txt"
    ]
