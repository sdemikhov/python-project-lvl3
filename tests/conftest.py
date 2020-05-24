import requests
import pytest

from pathlib import Path

TESTS_DIR = Path(__file__).parent.absolute()
FIXTURES_DIR = TESTS_DIR / 'fixtures'
TEST_PAGE_FILENAME = 'hexlet-io-courses.html'
TEST_URL = 'https://hexlet.io/courses'

SUCCESSFUL = 200
ERROR = 404

class MockResponse:
    def __init__(self, ok=True, text=None, status_code=SUCCESSFUL):
        self.ok = ok
        self.text = text
        self.status_code = status_code


@pytest.fixture
def test_page():
    page = {}

    with open(FIXTURES_DIR / TEST_PAGE_FILENAME) as f:
        page['content'] = f.read()

    page['filename'] = TEST_PAGE_FILENAME
    page['url'] = TEST_URL
    return page


@pytest.fixture
def mock_response_successful(monkeypatch, test_page):
    def mock_get(*args, **kwargs):
        return MockResponse(text=test_page['content'])

    monkeypatch.setattr(requests, "get", mock_get)


@pytest.fixture
def mock_response_error(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockResponse(ok=False, status_code=ERROR)

    monkeypatch.setattr(requests, "get", mock_get)
