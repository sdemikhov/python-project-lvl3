import re
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin

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
    soup = BeautifulSoup(response.text, features="html.parser")
    page_name = make_name(response.url, crop=SCHEME)
    tree[FILENAME] = page_name + EXTENSION
    tags_with_resources = soup.find_all(important_tag_has_local_src)
    if tags_with_resources:
        resources = []
        tree[RESOURCES_DIR] = Path(page_name + SUFFIX)
        for tag in tags_with_resources:
            resource_filename = make_name(
                tag[SRC],
                crop=SCHEME,
                extension=True
            )
            resource_url = urljoin(response.url, tag[SRC])
            resources.append((resource_filename, resource_url))
            new_src = tree[RESOURCES_DIR] / resource_filename
            tag[SRC] = new_src
        tree[RESOURCES] = resources
    tree[CONTENT] = str(soup)
    return tree


FILENAME_WITH_EXTENSION = r'(?P<name>.+)(?P<extension>\.[a-zA-Z0-9]+)'
NOT_LETTERS_OR_DIGITS = r'[^a-zA-Z0-9]'


def make_name(string, crop=None, extension=False):
    if crop is not None:
        string = re.sub(crop, '', string)
    if extension:
        parts = re.search(FILENAME_WITH_EXTENSION, string)
        if parts is not None:
            name = re.sub(
                NOT_LETTERS_OR_DIGITS,
                SEPARATOR,
                parts.group('name')
            )
            return name + parts.group('extension')
    return re.sub(NOT_LETTERS_OR_DIGITS, SEPARATOR, string)


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
