import logging

NONE = 'none'
WARNING = 'warning'
DEBUG = 'debug'


def setup(log_level):
    logger = logging.getLogger()
    console = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
    console.setFormatter(formatter)
    if log_level == NONE:
        level = logging.ERROR
    elif log_level == WARNING:
        level = logging.WARNING
    elif log_level == DEBUG:
        level = logging.DEBUG
    logger.setLevel(level)
    logger.addHandler(console)
