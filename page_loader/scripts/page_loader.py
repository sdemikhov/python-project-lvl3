import sys

from page_loader.cli import parser
from page_loader.page_loader import download_page
from page_loader import log
from page_loader.exceptions import PageLoaderError


def main():
    arguments = parser.parse_args()
    log.add_stream_handler(arguments.log_level)
    log.logger.debug(
        'User passed following arguments: {}'.format(arguments)
    )
    try:
        download_page(
            arguments.target_url,
            destination=arguments.destination,
        )
    except PageLoaderError as e:
        log.logger.error(str(e))
        if e.__cause__:
            log.logger.debug(e.__cause__)
        sys.exit(1)


if __name__ == "__main__":
    main()
