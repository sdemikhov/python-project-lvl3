import requests
from pathlib import Path
from progress.bar import Bar
from logging import getLogger

from page_loader.tree import (
    make_tree, FILENAME, RESOURCES, RESOURCES_DIR, CONTENT
)
from page_loader.exceptions import PageLoaderError
from page_loader import file


logger = getLogger()

DOWNLOADING = 'Downloading local resources'
RESPONSE_CODE_MESSAGE_TEMPATE = (
    "File '{url}' wasn't downloaded! Unacceptable response code '{code}'"
)
SUCCESSFUL_STATUS_CODE = 200
USER_AGENT = (
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
)


def download_page(target_url, destination=''):
    path = Path(destination)
    file.validate_dir(path)

    response = send_request(target_url)
    tree = make_tree(response)
    file.write_text(path / tree[FILENAME], tree[CONTENT])

    if tree[RESOURCES]:
        logger.warning(
            "Page '{}' has resources in '{}'".format(
                tree[FILENAME],
                tree[RESOURCES_DIR]
            )
        )
        resources_path = Path(path / tree[RESOURCES_DIR])
        progress_ = Bar(
                DOWNLOADING,
                max=len(tree[RESOURCES]),
                suffix='%(percent)d%%',
        )
        for filename, url_ in tree[RESOURCES]:
            resource_response = send_request(url_, stream=True)
            file.write_response(
                resources_path / filename,
                resource_response,
            )
            progress_.next()
        progress_.finish()


def send_request(url, stream=False):
    headers = {'User-Agent': USER_AGENT}
    try:
        logger.debug(
            "Sending request to url '{}'...".format(url)
        )
        response = requests.get(url, stream=stream, headers=headers)

    except (
        requests.exceptions.MissingSchema,
        requests.exceptions.ConnectionError,
        requests.exceptions.Timeout,
        requests.exceptions.TooManyRedirects
    ) as err:
        raise PageLoaderError(err) from err

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
