from twisted.internet import protocol, reactor
from twisted.web.client import Agent
from tcp_listener.adapter import Adapter
from tcp_listener import settings
from .request import request
from logging import getLogger

from twisted.internet.defer import setDebugging
setDebugging(True)

logger = getLogger()

agent = Agent(reactor)


class Server(protocol.Protocol):
    def dataReceived(self, data):
        logger.debug(data)
        try:
            datastring = data.decode()
        except UnicodeDecodeError:
            logger.exception(data)
            self.transport.loseConnection()
            return
        adapter = Adapter.detect(datastring)
        if adapter:
            message = adapter.decode(datastring)
            response = adapter.response_to(message)
            if response:
                logger.debug("response {}".format(response.encode()))
                self.transport.write(response.encode())
            request(agent, message.full_url)
        else:
            logger.error('UNKNOWN TRACKER {}'.format(data))
            # self.transport.loseConnection()

    def connectionLost(self, *args, **kwargs):
        logger.debug("DEVICE DISCONNECTED {} {}".format(args, kwargs))
        # self.transport.loseConnection()

    def connectionMade(self):
        logger.debug("DEVICE CONNECTED")


def start():
    logger.info('TCP Listener port {}'.format(settings.PORT))
    logger.info('URL to send requests {}'.format(settings.REQUEST_URL))
    factory = protocol.ServerFactory()
    factory.protocol = Server
    reactor.listenTCP(settings.PORT, factory)
    reactor.run()

