import requests
import pytest

from page_load import page_loader

TEMP_DIR = "test_page_loader_successful_responce"

def test_page_loader_successful_responce(
        tmp_path,
        mock_response_successful,
        test_page,
    ):

    destination = tmp_path / TEMP_DIR
    destination.mkdir()

    page_loader(test_page['url'], destination)
    saved_page = destination / test_page['filename']

    assert saved_page.exists(), "wrong filename or page doesn't saved"
    assert saved_page.read_text() == test_page['content'], (
        "Content of saved page is different"
    )


def test_page_loader_error_responce(mock_response_error, test_page):
    with pytest.raises(ValueError):
        page_loader(test_page['url'])
