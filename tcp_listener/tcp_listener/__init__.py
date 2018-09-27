import logging
from logging import _nameToLevel
import sys
from . import settings
logging.basicConfig(stream=sys.stdout, level=_nameToLevel[settings.LOG_LEVEL])


def run():
    from .listener import start
    start()
