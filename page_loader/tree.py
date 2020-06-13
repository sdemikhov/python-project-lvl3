import re
from pathlib import Path
from bs4 import BeautifulSoup
import urllib
from logging import getLogger

logger = getLogger()

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
LOCAL_RESOURCES = re.compile(r'^\.?/|^\w+/')
SCHEME = re.compile(r'^.+://|^\.?//?')
FILENAME_WITH_EXTENSION = re.compile(
    r'(?P<name>.+)(?P<extension>\.[a-zA-Z0-9]+$)'
)
NOT_LETTERS_OR_DIGITS = re.compile(r'[^a-zA-Zа-яА-Я0-9]')
SEPARATOR = '-'
MAX_LENGTH = 143


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
    tree[RESOURCES_DIR] = Path(page_name + SUFFIX)
    for tag in tags_with_resources:
        logger.debug("Local resource found: '{}'".format(tag))
        attribute_name = IMPORTANT_TAGS[tag.name]
        resource_url = urllib.parse.urljoin(
            response.url,
            tag[attribute_name]
        )
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


def make_name_from_url(url, extension=False):
    without_scheme = SCHEME.sub('', urllib.parse.unquote(url))
    cropped_end = re.sub(r'/$', '', without_scheme)
    if extension:
        parts = FILENAME_WITH_EXTENSION.search(cropped_end)
        if parts is not None:
            name = NOT_LETTERS_OR_DIGITS.sub(
                SEPARATOR,
                parts.group('name')
            )
            name_len = MAX_LENGTH - len(parts.group('extension'))
            return name[:name_len] + parts.group('extension')
    return NOT_LETTERS_OR_DIGITS.sub(
        SEPARATOR,
        cropped_end
    )[:MAX_LENGTH]


def important_tag_has_local_resource(tag):
    return (
        tag.name in IMPORTANT_TAGS and
        tag.has_attr(IMPORTANT_TAGS[tag.name]) and
        LOCAL_RESOURCES.search(tag.get(IMPORTANT_TAGS[tag.name]))
    )
