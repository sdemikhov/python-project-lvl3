import re
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from page_load.log import logger

SEPARATOR = '-'
EXTENSION = '.html'
SUFFIX = '_files'
SCHEME = r'^.+://|^\.?/'
FILENAME = 'filename'
RESOURCES = 'resources'
RESOURCES_DIR = 'resources_dir'
CONTENT = 'content'
SRC = 'src'


def make_tree(response):
    tree = {}
    logger.debug(
        "Start making tree for page '{}'...".format(response.url)
    )
    soup = BeautifulSoup(response.text, features="html.parser")
    page_name = make_name_from_url(response.url)
    tree[FILENAME] = page_name + EXTENSION
    tags_with_resources = soup.find_all(important_tag_has_local_src)
    resources = []
    if tags_with_resources:
        tree[RESOURCES_DIR] = Path(page_name + SUFFIX)
        for tag in tags_with_resources:
            logger.debug(
                "Local resource found '{}'".format(tag[SRC])
            )
            resource_filename = make_name_from_url(
                tag[SRC],
                extension=True
            )
            resource_url = urljoin(response.url, tag[SRC])
            resources.append((resource_filename, resource_url))
            new_src = tree[RESOURCES_DIR] / resource_filename
            tag[SRC] = new_src
    tree[RESOURCES] = resources
    tree[CONTENT] = str(soup)
    logger.debug(
        "Tree successfuly completed."
    )
    return tree


FILENAME_WITH_EXTENSION = r'(?P<name>.+)(?P<extension>\.[a-zA-Z0-9]+)'
NOT_LETTERS_OR_DIGITS = r'[^a-zA-Z0-9]'


def make_name_from_url(url, extension=False):
    without_scheme = re.sub(SCHEME, '', url)
    cropped_end = re.sub(r'/$', '', without_scheme)
    if extension:
        parts = re.search(FILENAME_WITH_EXTENSION, cropped_end)
        if parts is not None:
            name = re.sub(
                NOT_LETTERS_OR_DIGITS,
                SEPARATOR,
                parts.group('name')
            )
            return name + parts.group('extension')
    return re.sub(NOT_LETTERS_OR_DIGITS, SEPARATOR, cropped_end)


IMPORTANT_TAGS = [
    'link',
    'script',
    'img',
]
LOCAL_RESOURCES = r'^\.?/|^\w+/'


def important_tag_has_local_src(tag):
    return (
        tag.name in IMPORTANT_TAGS and
        tag.has_attr('src') and
        re.search(LOCAL_RESOURCES, tag['src'])
    )
