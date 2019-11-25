import os

import pytest

from victoria_smoke import template

from test_attachments import library, mock_open, mock_os_funcs, get_filenames


def test_create_environment():
    env = template.create_environment()
    assert hasattr(env, "filterfunc")


def test_emit_yaml_array():
    arr = template._emit_yaml_array(["one", "two", "three"])
    assert arr == "- one\n- two\n- three"


def test_process(library):
    EMAIL_TEMPLATE = """{{ library | filename("root_file_1.txt") | to_array }}"""

    result = template.process(EMAIL_TEMPLATE, library)
    assert result == f"- root_file_1.txt"


def test_to_array(library):
    filtered = library.get_filename("root_file_1.txt")
    result = template.to_array(filtered)
    assert result == "- root_file_1.txt"

    with pytest.raises(TypeError):
        template.to_array("wrong type")


def test_collapse():
    result = template.collapse(["one", "two", "three"])
    assert result == "one\n  two\n  three"


def test_to_ascii():
    result = template.to_ascii(bytes("hello", "ascii"))
    assert result == "hello"


def test_filename(library):
    with pytest.raises(TypeError):
        template.filename("wrong type", "test")

    result = template.filename(library, "root_file_1.txt")
    assert get_filenames(result) == ["root_file_1.txt"]


def test_like(library):
    with pytest.raises(TypeError):
        template.like("wrong type", "test")

    result = template.like(library, "root_file")
    assert get_filenames(result) == ["root_file_1.txt", "root_file_2.txt"]


def test_filetype(library):
    with pytest.raises(TypeError):
        template.filetype("wrong type", "test")

    result = template.filetype(library, "pdf")
    assert get_filenames(result) == ["pdf_file.pdf"]


def test_directory(library):
    with pytest.raises(TypeError):
        template.directory("wrong type", "test")

    result = template.directory(library, "subdir")
    assert get_filenames(result) == [
        f"subdir{os.sep}subfile_1.txt", f"subdir{os.sep}subfile_2.txt"
    ]


def test_filesize(library):
    with pytest.raises(TypeError):
        template.filesize("wrong type", "")

    result = template.filesize(library, minimum="1.1kb", maximum="2kb")
    assert get_filenames(result) == ["big_file.txt"]


def test_randomly_pick(library):
    with pytest.raises(TypeError):
        template.randomly_pick("wrong type", 1)

    # we need to specify the seed here to make the test deterministic
    result = template.randomly_pick(library, 2, seed=1337)
    assert get_filenames(result) == ["pdf_file.pdf", "big_file.txt"]
