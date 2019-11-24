from faker import Faker
import pytest
import unicodedata

from victoria_smoke.faker_text_provider import TextProvider


@pytest.fixture
def faker():
    fake = Faker()
    fake.add_provider(TextProvider)
    return fake


def test_fake_unicode(faker):
    result = faker.unicode(1000)
    assert len(result) == 1000


def test_fake_ascii(faker):
    result = faker.ascii(1000)
    assert len(result) == 1000