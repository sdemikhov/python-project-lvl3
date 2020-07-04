import requests
from pathlib import Path
from progress.bar import Bar
import logging
import re
from bs4 import BeautifulSoup
import urllib
import collections


DOWNLOADING = 'Downloading local resources'

SUCCESSFUL_STATUS_CODE = 200
USER_AGENT = (
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
)

EXTENSION = '.html'
SUFFIX = '_files'
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
MAX_FILENAME_LENGTH = 255

names_counter = collections.Counter()


class PageLoaderError(Exception):
    pass


class PageLoaderNetworkError(PageLoaderError):
    pass


class PageLoaderDirectoryError(PageLoaderError):
    pass


class PageLoaderFileError(PageLoaderError):
    pass


def download_page(target_url, destination=''):
    path = Path(destination)

    page_content, page_binary, response_url = send_request(target_url)

    prepared = parse_and_process_page(page_content, response_url)
    page, page_filename, resources = prepared

    write_to_file(
        path / page_filename,
        page,
        binary_mode=page_binary,
    )

    if resources:
        progress_ = Bar(
            DOWNLOADING,
            max=len(resources),
            suffix='%(percent)d%%',
        )

        resources_download_fail = []
        for url_, resource_filename in resources:
            try:
                resource_content, resource_binary, _ = send_request(url_)
            except PageLoaderError as err:
                logging.error(err)
                resources_download_fail.append(url_)
            else:
                write_to_file(
                    path / resource_filename,
                    resource_content,
                    binary_mode=resource_binary,
                )
            progress_.next()

        progress_.finish()
        if resources_download_fail:
            logging.warning(
                "Some resources are wasn't downloaded: '{}'".format(
                    ', '.join(resources_download_fail)
                )
            )


def send_request(url):
    headers = {'User-Agent': USER_AGENT}
    try:
        response = requests.get(url, headers=headers)
        if response.encoding:
            content = response.text
            binary = False
        else:
            content = response.content
            binary = True
    except requests.exceptions.MissingSchema as err:
        raise PageLoaderNetworkError(
            "Selected url doesn't contains schema (http://, https://...)!"
        ) from err
    except requests.exceptions.ConnectionError as err:
        raise PageLoaderNetworkError(
            (
                "An error occurred while trying to connect,"
                " check the correctness of url!"
            )
        ) from err
    except requests.exceptions.Timeout as err:
        raise PageLoaderNetworkError(
            "The requested resource does not respond for a long time!"
        ) from err
    except requests.exceptions.TooManyRedirects as err:
        raise PageLoaderNetworkError(
            "Many redirects occurred while accessing the resource"
        ) from err

    if response.status_code != SUCCESSFUL_STATUS_CODE:
        raise PageLoaderNetworkError(
            (
                "File '{url}' wasn't downloaded!"
                " Unacceptable response code '{code}'"
            ).format(url=url, code=response.status_code)
        )
    return (content, binary, response.url)


def parse_and_process_page(decoded_html, url):
    soup = BeautifulSoup(decoded_html, features="html.parser")

    base_for_name = make_name_from_url(url)
    page_filename = base_for_name + EXTENSION
    resources_dir = Path(base_for_name + SUFFIX)

    resources = []
    tags_with_resources = soup.find_all(important_tag_has_local_resource)
    for tag in tags_with_resources:
        logging.debug("Local resource found: '{}'".format(tag))
        attribute_name = IMPORTANT_TAGS[tag.name]
        resource_url = urllib.parse.urljoin(
            url,
            tag[attribute_name]
        )

        if resource_url == url:
            logging.debug(
                "Resource url == page url! Skip resource: '{}'".format(tag)
            )
            continue

        resource_filename = resources_dir / make_name_from_url(
            tag[attribute_name],
            search_extension=True
        )
        resources.append((resource_url, resource_filename))
        new_value = resource_filename
        tag[attribute_name] = new_value

    return (str(soup), page_filename, resources)


def make_name_from_url(url, search_extension=False):
    url_without_scheme = SCHEME.sub('', urllib.parse.unquote(url))
    cleared_url = re.sub(r'/$', '', url_without_scheme)

    if search_extension:
        parts = FILENAME_WITH_EXTENSION.search(cleared_url)
        if parts is not None:
            short_name = make_short_name(
                    NOT_LETTERS_OR_DIGITS.sub(SEPARATOR, parts.group('name')),
                    parts.group('extension')
            )
            if short_name:
                return short_name

    return make_short_name(
            NOT_LETTERS_OR_DIGITS.sub(SEPARATOR, cleared_url),
            ''
    )


def make_short_name(name, extension):
    result = ''

    name_bytes = name.encode()
    extension_bytes = extension.encode()

    if len(extension_bytes) >= MAX_FILENAME_LENGTH:
        return result

    length = MAX_FILENAME_LENGTH - len(extension_bytes)
    expected_name = name_bytes[:length] + extension_bytes

    filename_number = names_counter[expected_name]

    if filename_number == 0:
        result = expected_name.decode(errors='ignore')
    else:
        filename_number_bytes = str(filename_number).encode()
        length -= len(filename_number_bytes)
        if length <= 0:
            return result
        result = (
            name_bytes[:length] + filename_number_bytes + extension_bytes
        ).decode(errors='ignore')

    names_counter[expected_name] += 1
    return result


def important_tag_has_local_resource(tag):
    return (
        tag.name in IMPORTANT_TAGS and
        tag.has_attr(IMPORTANT_TAGS[tag.name]) and
        LOCAL_RESOURCES.search(tag.get(IMPORTANT_TAGS[tag.name]))
    )


def write_to_file(path_to_file, data, binary_mode=False):
    path = Path(path_to_file)

    make_directory(path)
    try:
        with open(path, 'wb' if binary_mode else 'w') as f:
            f.write(data)
    except OSError as err:
        raise PageLoaderFileError(
            (
                "An error occured while writing to file '{}',"
                " use debug mode for more info."
            ).format(path)
        ) from err


def make_directory(path_to_file):
    path = Path(path_to_file)

    try:
        path.parent.mkdir(parents=True, exist_ok=True)
    except NotADirectoryError as err:
        raise PageLoaderDirectoryError(
            "'{}' is not a directory!".format(path)
        ) from err
    except PermissionError as err:
        raise PageLoaderDirectoryError(
            "Can't create '{}' permission denied".format(path)
        ) from err
    except FileExistsError as err:
        raise PageLoaderDirectoryError(
            "Last path component is an existing non-directory file"
        ) from err
