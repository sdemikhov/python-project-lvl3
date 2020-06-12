from page_loader.log import logger


class PageLoaderError(Exception):
    @classmethod
    def raise_from(cls, exception, user_message=None):
        if user_message is not None:
            logger.error(user_message)
        else:
            logger.error(exception)
        logger.debug(exception, exc_info=True)
        raise cls(exception) from exception
