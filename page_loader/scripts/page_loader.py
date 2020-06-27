import sys
import traceback
import logging

from page_loader import cli, core
from page_loader import logging as pl_logging

SUCCESSFUL_EXIT_CODE = 0
COMMON_ERROR_EXIT_CODE = 1
NETWORK_ERROR_EXIT_CODE = 2
DIRECTORY_ERROR_EXIT_CODE = 3
FILE_ERROR_EXIT_CODE = 4


def main():
    arguments = cli.parser.parse_args()
    pl_logging.setup(arguments.log_level)
    logging.debug(
        'User passed following arguments: {}'.format(arguments)
    )
    try:
        core.download_page(
            arguments.target_url,
            destination=arguments.destination,
        )
    except core.PageLoaderError as e:
        logging.error(str(e))
        if e.__cause__:
            exception_cause = traceback.format_exception(
                etype=type(e.__cause__),
                value=e.__cause__,
                tb=e.__cause__.__traceback__
            )
            logging.debug(''.join(exception_cause))
        if isinstance(e, core.PageLoaderNetworkError):
            sys.exit(NETWORK_ERROR_EXIT_CODE)
        elif isinstance(e, core.PageLoaderNetworkError):
            sys.exit(DIRECTORY_ERROR_EXIT_CODE)
        elif isinstance(e, core.PageLoaderNetworkError):
            sys.exit(FILE_ERROR_EXIT_CODE)
        else:
            sys.exit(COMMON_ERROR_EXIT_CODE)
    sys.exit(SUCCESSFUL_EXIT_CODE)


if __name__ == "__main__":
    main()
