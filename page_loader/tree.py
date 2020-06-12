import re
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin, unquote

from page_loader.log import logger


EXTENSION = '.html'
SUFFIX = '_files'
FILENAME = 'filename'
RESOURCES = 'resources'
RESOURCES_DIR = 'resources_dir'
CONTENT = 'content'
IMPORTANT_TAGS = {
    'link': 'href',
    'script': 'src',
    'img': 'src',
}


def make_tree(response):
    tree = {}
    logger.debug(
        "Start making tree for page '{}'...".format(response.url)
    )
    soup = BeautifulSoup(response.text, features="html.parser")
    page_name = make_name_from_url(response.url)
    tree[FILENAME] = page_name + EXTENSION
    tags_with_resources = soup.find_all(important_tag_has_local_resource)
    resources = []
    if tags_with_resources:
        tree[RESOURCES_DIR] = Path(page_name + SUFFIX)
        for tag in tags_with_resources:
            logger.debug("Local resource found: '{}'".format(tag))
            attribute_name = IMPORTANT_TAGS[tag.name]
            resource_url = urljoin(response.url, tag[attribute_name])
            if resource_url == response.url:
                logger.debug(
                    "Resource url == page url! Skip resource: '{}'".format(tag)
                )
                continue
            resource_filename = make_name_from_url(
                tag[attribute_name],
                extension=True
            )
            resources.append((resource_filename, resource_url))
            new_value = tree[RESOURCES_DIR] / resource_filename
            tag[attribute_name] = new_value
    tree[RESOURCES] = resources
    tree[CONTENT] = str(soup)
    logger.debug(
        "Tree successfuly completed."
    )
    return tree


SCHEME = r'^.+://|^\.?//?'
FILENAME_WITH_EXTENSION = r'(?P<name>.+)(?P<extension>\.[a-zA-Z0-9]+$)'
NOT_LETTERS_OR_DIGITS = r'[^a-zA-Zа-яА-Я0-9]'
SEPARATOR = '-'
MAX_LENGTH = 143


def make_name_from_url(url, extension=False):
    without_scheme = re.sub(SCHEME, '', unquote(url))
    cropped_end = re.sub(r'/$', '', without_scheme)
    if extension:
        parts = re.search(FILENAME_WITH_EXTENSION, cropped_end)
        if parts is not None:
            name = re.sub(
                NOT_LETTERS_OR_DIGITS,
                SEPARATOR,
                parts.group('name')
            )
            name_len = MAX_LENGTH - len(parts.group('extension'))
            return name[:name_len] + parts.group('extension')
    return re.sub(
        NOT_LETTERS_OR_DIGITS, SEPARATOR,
        cropped_end
    )[:MAX_LENGTH]


LOCAL_RESOURCES = r'^\.?/|^\w+/'


def important_tag_has_local_resource(tag):
    return (
        tag.name in IMPORTANT_TAGS and
        tag.has_attr(IMPORTANT_TAGS[tag.name]) and
        re.search(LOCAL_RESOURCES, tag.get(IMPORTANT_TAGS[tag.name]))
    )
