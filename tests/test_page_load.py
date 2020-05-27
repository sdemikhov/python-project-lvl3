import requests
import pytest

from page_load import page_loader

TEMP_DIR = "test_page_loader_successful_responce"


def test_page_loader_successful_responce(
        tmp_path,
        mock_response_successful,
        test_page,
        result,
        resource,
    ):

    destination = tmp_path / TEMP_DIR
    destination.mkdir()

    page_loader(test_page.url, destination)
    
    saved_page_path = destination / result.filename
    saved_page_resource_path = (
        destination / resource.directory / resource.filename
    )
    assert saved_page_path.exists(), (
        "wrong page filename or page doesn't saved"
    )

    assert saved_page_resource_path.exists(), (
        "wrong page resource filename or resource doesn't saved"
    )

    assert saved_page_resource_path.read_text() == resource.content, (
        "Content of saved page resource is different"
    )


def test_page_loader_error_responce(mock_response_error, test_page):
    with pytest.raises(ValueError):
        page_loader(test_page.url)
