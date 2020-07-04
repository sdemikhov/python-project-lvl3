import requests
import pytest

from page_loader import core


def test_send_request_response_404(requests_mock, test_page):
    requests_mock.get(test_page.url, status_code=404)
    with pytest.raises(core.PageLoaderNetworkError):
        core.send_request(test_page.url)


def test_send_request_connection_error(
        mock_response_connection_error,
        test_page
    ):
    with pytest.raises(core.PageLoaderNetworkError):
        core.send_request(test_page.url)


def test_send_request_response_timeout(mock_response_timeout, test_page):
    with pytest.raises(core.PageLoaderNetworkError):
        core.send_request(test_page.url)


def test_send_request_many_redirects(
        mock_response_many_redirects,
        test_page
    ):
    with pytest.raises(core.PageLoaderNetworkError):
        core.send_request(test_page.url)
