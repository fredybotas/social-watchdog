import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%d %H:%M",
)


def get_logger(name):
    logger = logging.getLogger(name)
    return logger
