from page_loader.log import logger
from page_loader.exceptions import PageLoaderError


def validate_dir(path):
    if not path.exists():
        logger.error('No such file or directory: {}'.format(path))
        logger.debug(
            'No such file or directory: {}'.format(path),
            exc_info=True,
        )
        raise PageLoaderError(
            'No such file or directory: {}'.format(path)
        )
    if not path.is_dir():
        logger.error('Not a directory: {}'.format(path))
        logger.debug(
            'Not a directory: {}'.format(path),
            exc_info=True,
        )
        raise PageLoaderError(
            'Not a directory: {}'.format(path)
        )
    return True


def write_text(path, data):
    try:
        with open(path, 'w') as page:
            logger.debug('Saving page into: {}'.format(path))
            page.write(data)
            logger.debug("Page saved successfuly.")
    except (FileNotFoundError, PermissionError, NotADirectoryError) as err:
        PageLoaderError.raise_from(err)


def write_response(path, response):
    try:
        if not path.parent.exists():
            logger.warning(
                "Directory '{}' doesn`t exist"
                " start making directory...".format(path.parent)
            )
            path.parent.mkdir()
            logger.warning("Directory created sucessfuly.")

        if response.encoding:
            reading_mode = 'w'
            decode_unicode = True
        else:
            reading_mode = 'wb'
            decode_unicode = False

        with open(path, reading_mode) as f:
            logger.debug('Saving file into: {}'.format(path))
            for line in response.iter_content(
                decode_unicode=decode_unicode,
            ):
                f.write(line)
            logger.debug(
                "File saved successfuly."
            )
    except (
        FileNotFoundError,
        PermissionError,
        NotADirectoryError
    ) as err:
        PageLoaderError.raise_from(err)
