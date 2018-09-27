import logging
from tcp_listener.settings import TOKEN
logger = logging.getLogger()

from twisted.web.client import Headers


def request(agent, url: str):
    logger.debug(url)
    r = agent.request(b'GET', url.encode(), Headers({"Authorization": [TOKEN]}))
    r.addBoth(lambda p: logger.debug(p))
    # r.addErrback(lambda status: logger.error(status))
    # r.addCallback(lambda status: logger.debug("{} {}".format(status.code)))

