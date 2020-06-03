import sys

from page_load.cli import parser
from page_load.page_load import page_loader
from page_load import log
from page_load.exceptions import PageLoaderError


def main():
    arguments = parser.parse_args()
    log.add_stream_handler(arguments.log_level)
    log.logger.debug(
        'User passed following arguments: {}'.format(arguments)
    )
    try:
        page_loader(
            arguments.target_url,
            destination=arguments.destination,
        )
    except PageLoaderError:
        sys.exit(1)


if __name__ == "__main__":
    main()
