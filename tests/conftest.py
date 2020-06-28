import requests
import pytest
from collections import namedtuple
import builtins
from pathlib import Path

from page_loader import logging



TESTS_DIR = Path(__file__).parent.absolute()
FIXTURES_DIR = TESTS_DIR / 'fixtures'

PAGE_FILENAME = 'courses.html'
PAGE_URL = 'https://ru.hexlet.io/courses'


RESULT_FILENAME = 'ru-hexlet-io-courses.html'

RESOURCE_DIR = 'ru-hexlet-io-courses_files'
RESOURCE_URL = (
    'https://ru.hexlet.io/cdn-cgi/scripts'
    '/5c5dd728/cloudflare-static/email-decode.min.js'
)
RESOURCE_FILENAME = (
    'cdn-cgi-scripts-5c5dd728-cloudflare-static-email-decode-min.js'
)


def make_page(path, filename, url=None, directory=None):
    Page = namedtuple(
        'Page',
        'path, filename, url, directory, content'
    )

    with open(path / filename) as f:
        content = f.read()
    return Page(path, filename, url, directory, content)


@pytest.fixture(autouse=True)
def enable_log():
    logging.setup(logging.DEBUG)


@pytest.fixture
def test_page():
    return make_page(
        FIXTURES_DIR,
        PAGE_FILENAME,
        url=PAGE_URL
    )


@pytest.fixture
def expected_page():
    return make_page(
        FIXTURES_DIR,
        RESULT_FILENAME,
    )


@pytest.fixture
def expected_resource():
    return make_page(
        FIXTURES_DIR / RESOURCE_DIR,
        RESOURCE_FILENAME,
        url=RESOURCE_URL,
        directory=RESOURCE_DIR,
    )


@pytest.fixture
def mock_response_missing_schema(monkeypatch):
    def mock_get(*args, **kwargs):
        raise requests.exceptions.MissingSchema
        return None

    monkeypatch.setattr(requests, "get", mock_get)


@pytest.fixture
def mock_response_connection_error(monkeypatch):
    def mock_get(*args, **kwargs):
        raise requests.exceptions.ConnectionError
        return None

    monkeypatch.setattr(requests, "get", mock_get)


@pytest.fixture
def mock_response_timeout(monkeypatch):
    def mock_get(*args, **kwargs):
        raise requests.exceptions.Timeout
        return None

    monkeypatch.setattr(requests, "get", mock_get)


@pytest.fixture
def mock_response_many_redirects(monkeypatch):
    def mock_get(*args, **kwargs):
        raise requests.exceptions.TooManyRedirects
        return None

    monkeypatch.setattr(requests, "get", mock_get)


@pytest.fixture
def mock_open_dir_not_exists(monkeypatch):
    def mock_open(*args, **kwargs):
        raise FileNotFoundError
        return None

    monkeypatch.setattr(builtins, "open", mock_open)


@pytest.fixture
def mock_open_permisson_denied(monkeypatch):
    def mock_open(*args, **kwargs):
        raise PermissionError
        return None

    monkeypatch.setattr(builtins, "open", mock_open)
