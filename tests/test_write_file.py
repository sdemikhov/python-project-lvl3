import requests
import pytest

from page_loader import core

TEMP_DIR = "test_page_loader_successful_responce"


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
