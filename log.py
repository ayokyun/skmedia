import logging


LEVELS = {
    logging.DEBUG,
    logging.INFO,
    logging.WARNING,
    logging.ERROR,
    logging.CRITICAL
}


logger = logging.getLogger("ds")

LOGGING_LEVEL = logging.DEBUG
logger.setLevel(LOGGING_LEVEL)

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

stream_hander = logging.StreamHandler()
stream_hander.setFormatter(formatter)
logger.addHandler(stream_hander)

file_handler = logging.FileHandler('my.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


if __name__ == '__main__':

    logger.debug("debug")
    logger.info("info")
    logger.warning("warning")
    logger.error("error")
    logger.critical("critical")
# 출처: http://hamait.tistory.com/880 [HAMA 블로그]
