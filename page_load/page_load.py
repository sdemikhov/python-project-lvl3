import requests


from page_load.tree import (
    make_tree, FILENAME, RESOURCES, RESOURCES_DIR, CONTENT
)
from page_load import file
from page_load.log import logger


def page_loader(target_url, destination=None):
    response = send_request(target_url)
    tree = make_tree(response)

    path = file.make_dir(destination)
    with open(path / tree[FILENAME], 'w') as page:
        page.write(tree[CONTENT])
        logger.debug(
            "Page '{}' saved successful.".format(tree[FILENAME])
        )
    if tree[RESOURCES]:
        logger.debug(
            "Page '{}' contains local resources, need more requests...".format(
                tree[FILENAME]
            )
        )
        resources_path = file.make_dir(path / tree[RESOURCES_DIR])
        for filename, url_ in tree[RESOURCES]:
            resource_response = send_request(url_)
            with open(resources_path / filename, 'w') as resource:
                resource.write(resource_response.text)
                logger.debug(
                    "Resource '{}' saved successful.".format(filename)
                )


MESSAGE_TEMPATE = "File '{url}' wasn't downloaded! Response code '{code}'"


def send_request(url):
    logger.debug(
        "Sending request to url '{}'...".format(url)
    )
    response = requests.get(url)
    if response.ok:
        logger.debug(
            "Response recived, code: '{code}'.".format(
                code=response.status_code
            )
        )
        return response
    else:
        raise ValueError(
            MESSAGE_TEMPATE.format(url=url, code=response.status_code)
        )
