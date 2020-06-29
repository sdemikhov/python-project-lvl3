import requests
import pytest
from bs4 import BeautifulSoup

from page_loader import core

TEMP_DIR = "test_page_loader_successful_responce"


def test_download_page_responce_successful(
        tmp_path,
        requests_mock,
        test_page,
        expected_page,
        expected_resource,
    ):
    destination = tmp_path / TEMP_DIR
    destination.mkdir()

    requests_mock.get(test_page.url, text=test_page.content)
    requests_mock.get(
        expected_resource.url,
        content=expected_resource.content.encode()
    )
    core.download_page(test_page.url, destination)

    saved_page_path = destination / expected_page.filename
    saved_page_resource_path = (
        destination / expected_resource.directory / expected_resource.filename
    )
    assert saved_page_path.exists(), (
        "wrong page filename or page doesn't saved"
    )

    assert saved_page_resource_path.exists(), (
        "wrong page resource filename or resource doesn't saved"
    )

    saved_soup = BeautifulSoup(
        saved_page_path.read_text(),
        features="html.parser"
    )
    expected_soup = BeautifulSoup(expected_page.content, features="html.parser")

    assert saved_soup == expected_soup, (
        "Content of saved page is different"
    )

    assert saved_page_resource_path.read_text() == expected_resource.content, (
        "Content of saved page resource is different"
    )


def test_send_request_response_404(requests_mock, test_page):
    requests_mock.get(test_page.url, text=test_page.content, status_code=404)
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


def test_make_directory_permission_denied(
        tmp_path,
        mock_path_permisson_denied,
    ):
    destination = tmp_path / TEMP_DIR

    with pytest.raises(core.PageLoaderDirectoryError):
        core.make_directory(destination)


def test_make_directory_not_a_directory(
        tmp_path,
        mock_path_not_a_directory,
    ):
    destination = tmp_path / TEMP_DIR

    with pytest.raises(core.PageLoaderDirectoryError):
        core.make_directory(destination)


def test_make_directory_file_exists_error(
        tmp_path,
        mock_path_file_exists_error,
    ):
    destination = tmp_path / TEMP_DIR

    with pytest.raises(core.PageLoaderDirectoryError):
        core.make_directory(destination)


def test_make_directory_file_exists_error(
        tmp_path,
        mock_path_file_exists_error,
    ):
    destination = tmp_path / TEMP_DIR

    with pytest.raises(core.PageLoaderDirectoryError):
        core.make_directory(destination)


def test_write_to_file_os_error(
        tmp_path,
        mock_open_oserror,
    ):
    destination = tmp_path / TEMP_DIR
    data = "test"

    with pytest.raises(core.PageLoaderFileError):
        core.write_to_file(destination, data)
