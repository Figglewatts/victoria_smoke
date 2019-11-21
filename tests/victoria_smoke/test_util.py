from contextlib import nullcontext as does_not_raise

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