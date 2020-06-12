import sys
from logging import getLogger

from page_loader.cli import parser
from page_loader.page_loader import download_page
from page_loader import logging
from page_loader.exceptions import PageLoaderError


def main():
    arguments = parser.parse_args()
    logging.setup(arguments.log_level)
    logger = getLogger()
    logger.debug(
        'User passed following arguments: {}'.format(arguments)
    )
    try:
        download_page(
            arguments.target_url,
            destination=arguments.destination,
        )
    except PageLoaderError as e:
        logger.error(str(e))
        if e.__cause__:
            logger.debug(e.__cause__)
        sys.exit(1)


if __name__ == "__main__":
    main()
