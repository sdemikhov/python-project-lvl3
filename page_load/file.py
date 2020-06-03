from page_load.log import logger
from page_load.exceptions import PageLoaderError


def validate_dir(path):
    if not path.exists():
        logger.error('No such file or directory: {}'.format(path))
        raise PageLoaderError(
            'No such file or directory: {}'.format(path)
        )
    if not path.is_dir():
        logger.error('Not a directory: {}'.format(path))
        raise PageLoaderError(
            'Not a directory: {}'.format(path)
        )
    return True


def write_text(path, data):
    try:
        with open(path, 'w') as page:
            logger.debug('Save page into: {}...'.format(path))
            page.write(data)
            logger.debug("Page saved successfuly.")
    except (FileNotFoundError, PermissionError, NotADirectoryError) as err:
        PageLoaderError.raise_from(err)


def write_bytes(path, data):
    try:
        if not path.parent.exists():
            logger.warning(
                "Directory '{}' doesn`t exist"
                " start making directory...".format(path.parent)
            )
            path.parent.mkdir()
            logger.warning("Directorycreated sucessfuly.")
        with open(path, 'wb') as resource:
            logger.debug('Save resource into: {}...'.format(path))
            for chunk in data.iter_content():
                resource.write(chunk)
            logger.debug(
                "Resource saved successfuly."
            )
    except (FileNotFoundError, PermissionError, NotADirectoryError) as err:
        PageLoaderError.raise_from(err)
