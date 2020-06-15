import requests
from pathlib import Path
from progress.bar import Bar
import logging
import re
from bs4 import BeautifulSoup
import urllib
import collections

from page_loader.exceptions import PageLoaderError
from page_loader import file


logger = logging.getLogger()
names_counter = collections.Counter()

DOWNLOADING = 'Downloading local resources'
RESPONSE_CODE_MESSAGE_TEMPATE = (
    "File '{url}' wasn't downloaded! Unacceptable response code '{code}'"
)
SCHEMA_ERROR = "Selected url doesn't contains schema (http://, https://...)!"
CONNECTION_ERROR = (
    "An error occurred while trying to connect, check the correctness of url!"
)
TIMEOUT_ERROR = "The requested resource does not respond for a long time!"
REDIRECTS_ERROR = "Many redirects occurred while accessing the resource"
UKNOWN_ERROR = 'An unknown error occurred while processing the request'
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


def download_page(target_url, destination=''):
    path = Path(destination)
    file.validate_dir(path)

    response = send_request(target_url)

    (page_text, page_filename), resources = parse_page(response)
    file.write_text(path / page_filename, page_text)

    if resources:
        progress_ = Bar(
                DOWNLOADING,
                max=len(resources),
                suffix='%(percent)d%%',
        )

        resources_download_fail = []
        for url_, resource_filename in resources:
            try:
                resource_response = send_request(url_, stream=True)

                file.write_response(
                    path / resource_filename,
                    resource_response,
                )
            except PageLoaderError as err:
                logger.error(err)
                resources_download_fail.append(url_)
                resource_response.close()
            progress_.next()
        progress_.finish()
        if resources_download_fail:
            logger.warning(
                "Error while downloading resources: {}".format(
                    ', '.join(resources_download_fail)
                )
            )


def send_request(url, stream=False):
    headers = {'User-Agent': USER_AGENT}
    try:
        response = requests.get(url, stream=stream, headers=headers)

    except requests.exceptions.MissingSchema as err:
        raise PageLoaderError(SCHEMA_ERROR) from err
    except requests.exceptions.ConnectionError as err:
        raise PageLoaderError(CONNECTION_ERROR) from err
    except requests.exceptions.Timeout as err:
        raise PageLoaderError(TIMEOUT_ERROR) from err
    except requests.exceptions.TooManyRedirects as err:
        raise PageLoaderError(REDIRECTS_ERROR) from err
    except requests.exceptions.RequestException as err:
        raise PageLoaderError(UKNOWN_ERROR) from err

    if response.status_code == SUCCESSFUL_STATUS_CODE:
        return response
    logger.error(
        RESPONSE_CODE_MESSAGE_TEMPATE.format(
            url=url,
            code=response.status_code
        )
    )
    raise PageLoaderError(
        RESPONSE_CODE_MESSAGE_TEMPATE.format(
            url=url,
            code=response.status_code
        )
    )


def parse_page(response):
    logger.debug(
        "Start parsing page '{}'...".format(response.url)
    )
    soup = BeautifulSoup(response.text, features="html.parser")

    base_for_name = make_name_from_url(response.url)
    page_filename = base_for_name + EXTENSION
    resources_dir = Path(base_for_name + SUFFIX)

    resources = []
    tags_with_resources = soup.find_all(important_tag_has_local_resource)
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

        resource_filename = resources_dir / make_name_from_url(
            tag[attribute_name],
            search_extension=True
        )
        resources.append((resource_url, resource_filename))
        new_value = resource_filename
        tag[attribute_name] = new_value

    logger.debug(
        "Page successfuly parsed."
    )
    return (
        (str(soup), page_filename),
        tuple(resources),
    )


def make_name_from_url(url, search_extension=False):
    url_without_scheme = SCHEME.sub('', urllib.parse.unquote(url))
    cleared_url = re.sub(r'/$', '', url_without_scheme)

    if search_extension:
        parts = FILENAME_WITH_EXTENSION.search(cleared_url)
        if parts is not None:
            short_name = make_short_name(
                (
                    NOT_LETTERS_OR_DIGITS.sub(SEPARATOR, parts.group('name')),
                    parts.group('extension')
                )
            )
            if short_name:
                return short_name

    return make_short_name(
        (
            NOT_LETTERS_OR_DIGITS.sub(SEPARATOR, cleared_url),
            '',
        )
    )


def make_short_name(long_name_and_extension):
    result = ''

    name, extension = long_name_and_extension
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
