import requests
import pytest
from collections import namedtuple

from pathlib import Path

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


SUCCESSFUL = 200
ERROR = 404


def mock_response(ok=True, text=None, status_code=SUCCESSFUL, url=None):
    Response = namedtuple('Response', 'ok, text, status_code, url')
    return Response(ok, text, status_code, url)


def make_page(path, filename, url=None, directory=None):
    Page = namedtuple('Page', 'path, filename, url, directory, content')

    with open(path / filename) as f:
        content = f.read()
    return Page(path, filename, url, directory, content)


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
def mock_response_successful(monkeypatch, test_page, expected_resource):
    def mock_get(*args, **kwargs):
        if PAGE_URL in args:
            return mock_response(text=test_page.content, url=PAGE_URL)
        elif RESOURCE_URL in args:
            return mock_response(
                text=expected_resource.content,
                url=RESOURCE_URL
            )

    monkeypatch.setattr(requests, "get", mock_get)


@pytest.fixture
def mock_response_error(monkeypatch):
    def mock_get(*args, **kwargs):
        return mock_response(ok=False, status_code=ERROR)

    monkeypatch.setattr(requests, "get", mock_get)
