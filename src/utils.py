import logging


logging.basicConfig(format='"time(%(asctime)s) level(%(levelname)s) => %(message)s"',level=logging.DEBUG)
logger = logging.getLogger("logger")