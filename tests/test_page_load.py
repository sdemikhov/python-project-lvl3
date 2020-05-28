import requests
import pytest
from bs4 import BeautifulSoup

from page_load import page_loader

TEMP_DIR = "test_page_loader_successful_responce"


def test_page_loader_successful_responce(
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


def test_page_loader_error_responce(mock_response_error, test_page):
    with pytest.raises(ValueError):
        page_loader(test_page.url)
