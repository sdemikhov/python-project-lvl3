import requests
import re
from pathlib import Path

MESSAGE_TEMPATE = "Page wasn't downloaded! Responce code {}"


def page_loader(target_url, destination=None):
    request = requests.get(target_url)

    if request.ok:
        filename = make_filename(target_url)

        if destination is None:
            path = Path.cwd()
        else:
            path = Path(destination)

        with open(path / filename, 'w') as f:
            f.write(request.text)
    else:
        raise ValueError(
            MESSAGE_TEMPATE.format(request.status_code)
        )


SCHEME = r'^.*//'
NOT_LETTERS_OR_DIGITS = r'[^a-zA-Z0-9]'
SEPARATOR = '-'
EXTANSION = '.html'


def make_filename(target_url):
    url_without_scheme = re.sub(SCHEME, '', target_url)
    filename_without_extansion = re.sub(
        NOT_LETTERS_OR_DIGITS,
        SEPARATOR,
        url_without_scheme,
    )
    return filename_without_extansion + EXTANSION
