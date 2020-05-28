import logging

NONE = 'none'
WARNING = 'warning'
DEBUG = 'debug'

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def add_stream_handler(log_level):
    console = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
    console.setFormatter(formatter)
    if log_level == NONE:
        logger.setLevel(logging.NOTSET)
    elif log_level == WARNING:
        logger.setLevel(logging.WARNING)
    elif log_level == DEBUG:
        logger.setLevel(logging.DEBUG)
    logger.addHandler(console)
