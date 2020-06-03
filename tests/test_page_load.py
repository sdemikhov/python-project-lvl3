import requests
import pytest
from bs4 import BeautifulSoup

from page_load import page_loader
from page_load.exceptions import PageLoaderError

TEMP_DIR = "test_page_loader_successful_responce"


def test_page_loader_responce_successful(
        tmp_path,
        mock_response_successful,
        test_page,
        expected_page,
        expected_resource,
    ):
    destination = tmp_path / TEMP_DIR
    destination.mkdir()

    page_loader(test_page.url, destination)
    
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


def test_page_loader_response_404(mock_response_code_404, test_page):
    with pytest.raises(PageLoaderError):
        page_loader(test_page.url)


def test_page_loader_connection_error(
        mock_response_connection_error,
        test_page
    ):
    with pytest.raises(PageLoaderError):
        page_loader(test_page.url)


def test_page_loader_response_timeout(mock_response_timeout, test_page):
    with pytest.raises(PageLoaderError):
        page_loader(test_page.url)


def test_page_loader_many_redirects(
        mock_response_many_redirects,
        test_page
    ):
    with pytest.raises(PageLoaderError):
        page_loader(test_page.url)


def test_page_loader_dir_not_exists(
        tmp_path,
        mock_response_successful,
        mock_open_dir_not_exists,
        test_page,
    ):
    destination = tmp_path / TEMP_DIR

    with pytest.raises(PageLoaderError):
        page_loader(test_page.url, destination)


def test_page_loader_permission_denied(
        tmp_path,
        mock_response_successful,
        mock_open_permisson_denied,
        test_page,
    ):
    destination = tmp_path / TEMP_DIR

    with pytest.raises(PageLoaderError):
        page_loader(test_page.url, destination)
