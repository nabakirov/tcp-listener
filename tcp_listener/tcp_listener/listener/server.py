from twisted.internet import protocol, reactor, threads
from twisted.web.client import Agent
from .handler import handle_tracker
from tcp_listener import configs

agent = Agent(reactor)

counter = 0
connecteds = dict()
import logging
ids = dict()

class Server(protocol.Protocol):
    def dataReceived(self, data):
        id_ = self.id = self.id or data[1:13]
        
        if id_ in connecteds:
            if connecteds[id_] is not self:
                connecteds[id_].is_primary = False
                connecteds[id_].transport.loseConnection()
                connecteds[id_] = self
        else:
            connecteds[id_] = self
        d = threads.deferToThread(handle_tracker, data, agent)
        d.addErrback(print)
        self.transport.write(b'ok')
        if not ids.get(id_, None):
            ids[id_] = 1
            logging.debug('{}'.format(id_.decode()))

    def connectionLost(self, reason):
        global counter
        counter -= 1
        logging.info('{} disconnected {}'.format(counter, self.id))
        # del connecteds[self.id]
        self.transport.loseConnection()

    def connectionMade(self):
        global counter
        counter += 1
        self.id = None
        logging.info('{} connected'.format(counter))


def start():
    logging.info('port {}'.format(configs['LISTENER_PORT']))
    factory = protocol.ServerFactory()
    factory.protocol = Server
    reactor.listenTCP(configs['LISTENER_PORT'], factory)
    reactor.run()

