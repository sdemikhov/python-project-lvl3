import requests
import pytest
from collections import namedtuple
import builtins
from pathlib import Path

from page_loader import log



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


def mock_response(
        ok=True,
        text=None,
        iter_content=None,
        status_code=SUCCESSFUL,
        url=None,
        encoding='utf-8',
        headers={'Content-Length': '30'}
    ):
    Response = namedtuple(
        'Response',
        'ok, text, iter_content, status_code, url, encoding, headers'
    )
    return Response(
        ok,
        text,
        iter_content,
        status_code,
        url,
        encoding,
        headers,
    )


def make_iter_content(data):
    def inner(*args, **kwargs):
        return (line.encode() for line in data)
    return inner


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
    log.add_stream_handler(log.DEBUG)


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
                iter_content=make_iter_content(expected_resource.content),
                url=RESOURCE_URL,
                encoding=None,
            )

    monkeypatch.setattr(requests, "get", mock_get)


@pytest.fixture
def mock_response_code_404(monkeypatch):
    def mock_get(*args, **kwargs):
        return mock_response(ok=False, status_code=ERROR)

    monkeypatch.setattr(requests, "get", mock_get)


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
