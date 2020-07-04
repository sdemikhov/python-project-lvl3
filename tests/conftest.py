import requests
import pytest
import builtins
from pathlib import Path
import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
import socket
import threading
from jinja2 import Environment, FileSystemLoader

from page_loader import logging

TESTS_DIR = Path(__file__).parent.absolute()
FIXTURES_DIR = TESTS_DIR / 'fixtures'

ORIGINAL_PAGE_URL = 'http://127.0.0.1:{}/'
ORIGINAL_RESOURCES_PATHS = (
    FIXTURES_DIR / 'images/logo.png',
    FIXTURES_DIR / 'styles/style.css',
    FIXTURES_DIR / 'scripts/script.js',
)

EXPECTED_PAGE_TEMPLATE = 'expected_page.html'
EXPECTED_PAGE_FILENAME = '127-0-0-1-{}.html'

EXPECTED_RESOURCES_DIR = '127-0-0-1-{}_files'

EXPECTED_RESOURCES_PATHS = (
    'images-logo.png',
    'styles-style.css',
    'scripts-script.js',
)


@pytest.fixture(autouse=True)
def enable_log():
    logging.setup(logging.DEBUG)


class TestPage:
    def __init__(self, port):
        self.port = port

    @property
    def url(self):
        return ORIGINAL_PAGE_URL.format(self.port)

    @property
    def expected_filename(self):
        return EXPECTED_PAGE_FILENAME.format(self.port)

    @property
    def expected_resources_dir(self):
        return EXPECTED_RESOURCES_DIR.format(self.port)


    def get_resources_pairs(self):
        expected_resources = [Path(self.expected_resources_dir, p)
                              for p in EXPECTED_RESOURCES_PATHS]
        return [
            (o,e) for o, e in zip(ORIGINAL_RESOURCES_PATHS, expected_resources)
        ]


    def render_expected_page_text(self):
        env = Environment(loader=FileSystemLoader(FIXTURES_DIR / 'templates'))
        template = env.get_template(EXPECTED_PAGE_TEMPLATE)
        return template.render(port=self.port)


@pytest.fixture
def test_page():
    return TestPage


def get_free_port():
    s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
    s.bind(('localhost', 0))
    address, port = s.getsockname()
    s.close()
    return port


class Mock_Server:
    def _setup(self):
        self.port = get_free_port()
        os.chdir(FIXTURES_DIR)
        server_address = ('', self.port)
        server = HTTPServer(server_address, SimpleHTTPRequestHandler)
        self.server = server

    def run(self):
        self._setup()
        httpd_ = threading.Thread(target=self.server.serve_forever)
        httpd_.daemon = True
        httpd_.start()


@pytest.fixture
def mock_server():
    server = Mock_Server()
    server.run()
    return server


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
