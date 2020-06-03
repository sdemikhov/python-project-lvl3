import requests
from pathlib import Path

from page_load.tree import (
    make_tree, FILENAME, RESOURCES, RESOURCES_DIR, CONTENT
)
from page_load.log import logger
from page_load.exceptions import PageLoaderError
from page_load import file


def page_loader(target_url, destination=''):
    path = Path(destination)
    file.validate_dir(path)

    response = send_request(target_url)
    tree = make_tree(response)
    file.write_page(path / tree[FILENAME], tree[CONTENT])

    if tree[RESOURCES]:
        logger.warning(
            "Page '{}' has resources in '{}'".format(
                tree[FILENAME],
                tree[RESOURCES_DIR]
            )
        )
        resources_path = Path(path / tree[RESOURCES_DIR])
        for filename, url_ in tree[RESOURCES]:
            resource_response = send_request(url_, stream=True)
            file.write_resource(resources_path / filename, resource_response)


RESPONSE_CODE_MESSAGE_TEMPATE = (
    "File '{url}' wasn't downloaded! Unacceptable response code '{code}'"
)
SUCCESSFUL_STATUS_CODE = 200


def send_request(url, stream=False):
    try:
        logger.debug(
            "Sending request to url '{}'...".format(url)
        )
        response = requests.get(url, stream=stream)

    except (
        requests.exceptions.MissingSchema,
        requests.exceptions.ConnectionError,
        requests.exceptions.Timeout,
        requests.exceptions.TooManyRedirects
    ) as err:
        PageLoaderError.raise_from(err)

    if response.status_code == SUCCESSFUL_STATUS_CODE:
        logger.debug("Response recieved successfuly.")
        return response
    logger.error(
        RESPONSE_CODE_MESSAGE_TEMPATE.format(
            url=url,
            code=response.status_code
        )
    )
    logger.debug(
        RESPONSE_CODE_MESSAGE_TEMPATE.format(
            url=url,
            code=response.status_code
        ),
        exc_info=True,
    )
    raise PageLoaderError(
        RESPONSE_CODE_MESSAGE_TEMPATE.format(
            url=url,
            code=response.status_code
        )
    )
