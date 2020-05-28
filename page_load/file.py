from pathlib import Path
from page_load.log import logger


def make_dir(destination=None):
    logger.debug(
        'Start parsing directory path...'
    )
    if destination is None:
        path = Path.cwd()
        logger.debug(
            'Select CWD: {}.'.format(path)
        )
    else:
        path = Path(destination)
        logger.debug(
            'Select directory: {}.'.format(path)
        )
        if not path.exists():
            logger.warning(
                "Directory '{}' doesn`t exist"
                " start making directory...".format(path)
            )
            path.mkdir()
            logger.warning(
                "Directory created sucessfuly."
            )
    return path
