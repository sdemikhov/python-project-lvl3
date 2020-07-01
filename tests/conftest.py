import requests
import pytest
from collections import defaultdict
import builtins
from pathlib import Path
import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
import threading

from page_loader import logging



TESTS_DIR = Path(__file__).parent.absolute()
FIXTURES_DIR = TESTS_DIR / 'fixtures'

ORIGINAL_PAGE_FILENAME = 'index.html'
ORIGINAL_PAGE_URL = 'http://127.0.0.1:8000/'
ORIGINAL_RESOURCES_PATHS = (
    FIXTURES_DIR / '/images/logo.png',
    FIXTURES_DIR / '/styles/style.css',
    FIXTURES_DIR / '/scripts/script.js',
)


EXPECTED_PAGE_FILENAME = '127-0-0-1-8000.html'

EXPECTED_RESOURCES_DIR = '127-0-0-1-8000_files'

EXPECTED_RESOURCES_PATHS = (
    '127-0-0-1-8000/filesimages-logo.png',
    '127-0-0-1-8000_files/scripts-script.js',
    '127-0-0-1-8000_files/styles-style.css',
)


@pytest.fixture(autouse=True)
def enable_log():
    logging.setup(logging.DEBUG)


@pytest.fixture
def page():
    page = defaultdict(dict)

    page['original']['url'] = ORIGINAL_PAGE_URL
    page['original']['resources_paths'] = [
        path for path in ORIGINAL_RESOURCES_PATHS
    ]

    with open(FIXTURES_DIR / EXPECTED_PAGE_FILENAME) as e:
        page['expected']['text'] = e.read()
    page['expected']['filename'] = EXPECTED_PAGE_FILENAME

    page['expected']['resources_paths'] = [
        path for path in EXPECTED_RESOURCES_PATHS
    ]
    return page


def create_server():
    os.chdir(FIXTURES_DIR)
    server_address = ('', 8000)   
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)                                                                                                                                   
    httpd.serve_forever()


@pytest.fixture
def http_server():
    httpd_ = threading.Thread(target=create_server)
    httpd_.daemon = True
    httpd_.start()


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
def mock_path_permisson_denied(monkeypatch):
    def mock_path_make_dir(*args, **kwargs):
        raise PermissionError
        return None

    monkeypatch.setattr(Path, "mkdir", mock_path_make_dir)


@pytest.fixture
def mock_path_not_a_directory(monkeypatch):
    def mock_path_make_dir(*args, **kwargs):
        raise NotADirectoryError
        return None

    monkeypatch.setattr(Path, "mkdir", mock_path_make_dir)


@pytest.fixture
def mock_path_file_exists_error(monkeypatch):
    def mock_path_make_dir(*args, **kwargs):
        raise FileExistsError
        return None

    monkeypatch.setattr(Path, "mkdir", mock_path_make_dir)


@pytest.fixture
def mock_open_oserror(monkeypatch):
    def mock_open(*args, **kwargs):
        raise OSError
        return None

    monkeypatch.setattr(builtins, "open", mock_open)
