import pytest

from victoria_smoke import template


def test_create_environment():
    env = template.create_environment()
    assert hasattr(env, "filterfunc")


def test_emit_yaml_array():
    arr = template._emit_yaml_array(["one", "two", "three"])
    assert arr == "- one\n- two\n- three"
