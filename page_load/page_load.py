import re
from pathlib import Path
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin


EXTENSION = '.html'
SUFFIX = '_files'


def page_loader(target_url, destination=None):
    response = send_request(target_url)

    page_filename = make_name(target_url, truncate=SCHEME)

    soup = BeautifulSoup(response.text, features="html.parser")
    tags_with_resources = soup.find_all(important_tag_has_local_src)
    if tags_with_resources:
        resources = []
        resources_directory = Path(page_filename + SUFFIX)
        for tag in tags_with_resources:
            resource_filename = make_name(
                tag['src'],
                truncate=SCHEME,
                save_extension=True
            )
            resource_url = urljoin(target_url, tag['src'])
            resources.append((resource_filename, resource_url))
            new_src = resources_directory / resource_filename
            tag['src'] = new_src
    if destination is None:
        destination_path = Path.cwd()
    else:
        destination_path = Path(destination)
        if not destination_path.exists():
            destination_path.mkdir()
    with open(destination_path / (page_filename + EXTENSION), 'w') as f:
        f.write(soup.prettify())
    if resources:
        if not (destination_path / resources_directory).exists():
            (destination_path / resources_directory).mkdir()
        for resource_filename, resource_url in resources:
            resource_response = send_request(resource_url)
            with open(destination_path / resources_directory / resource_filename, 'w') as f:
                f.write(resource_response.text)


MESSAGE_TEMPATE = "File '{url}' wasn't downloaded! Response code '{code}'"


def send_request(url_):
    response = requests.get(url_)
    if response.ok:
        return response
    else:
        raise ValueError(
            MESSAGE_TEMPATE.format(url=url_, code=response.status_code)
        )


SCHEME = r'^.+://|^\.?/'
NOT_LETTERS_OR_DIGITS = r'[^a-zA-Z0-9]'
FILENAME_WITH_EXTENSION = '(?P<name>.+)(?P<extension>\.[a-zA-Z0-9]+)'
SEPARATOR = '-'


def make_name(string, truncate=None, save_extension=False):
    if truncate is not None:
        string = re.sub(truncate, '', string)
    if save_extension:
        parts = re.search(FILENAME_WITH_EXTENSION, string)
        if parts is not None:
            name =  re.sub(
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
