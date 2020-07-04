import pytest
from bs4 import BeautifulSoup

from page_loader import core

TEMP_DIR = "test_page_loader_successful_response"

def test_download_page_response_successful(
        tmp_path,
        mock_server,
        test_page
    ):
    destination = tmp_path / TEMP_DIR
    destination.mkdir()

    page = test_page(mock_server.port)

    core.download_page(page.url, destination)

    saved_page_path = destination / page.expected_filename
    assert saved_page_path.exists(), (
        "wrong page filename or page doesn't saved"
    )

    saved_soup = BeautifulSoup(
        saved_page_path.read_text(),
        features="html.parser"
    )
    saved_strings = list(saved_soup.stripped_strings)

    expected_soup = BeautifulSoup(
        page.render_expected_page_text(),
        features="html.parser"
    )
    expected_strings = list(expected_soup.stripped_strings)
    assert saved_strings == expected_strings, (
        "Content of saved page is different"
    )

    for original, expected in page.get_resources_pairs():
        with open(original, 'rb') as o, open(destination / expected, 'rb') as e:
            assert o.read() == e.read(), (
                'content of saved resources is different'
            )
