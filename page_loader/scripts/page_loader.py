import sys
from logging import getLogger
import traceback

from page_loader import cli, logging, core


def main():
    arguments = cli.parser.parse_args()
    logging.setup(arguments.log_level)
    logger = getLogger()
    logger.debug(
        'User passed following arguments: {}'.format(arguments)
    )
    try:
        core.download_page(
            arguments.target_url,
            destination=arguments.destination,
        )
    except core.PageLoaderError as e:
        logger.error(str(e))
        if e.__cause__:
            logger.debug(traceback.format_exc())

        if str(e).startswith(core.REQUEST_ERROR_PREFIX):
            sys.exit(2)
        elif str(e).startswith(core.DIRECTORY_ERROR_PREFIX):
            sys.exit(3)
        elif str(e).startswith(core.WRITE_ERROR_PREFIX):
            sys.exit(4)
        sys.exit(1)

    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
