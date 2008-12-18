from twisted.internet.protocol import Protocol

from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
from twisted.internet.tcp import Server as TStransport

import safe_store

END_LINE = "<*END_LINE*>"

class ServerTransport(TStransport):
    def __init__(self, sock, protocol, client, server, sessionno):
        TStransport.__init__(self, sock, protocol, client, server, sessionno)
        protocol.factory.all_transports.append(self)

class ServerProtocol(Protocol):

    def helper(self):
        return self.factory.helper

    def connectionMade(self):
        self.helper().newConnection(self.transport)

    def dataReceived(self, data):
        for d in data.split(END_LINE):
            self.helper().receiveData(self.transport, safe_store.load(d))

    def connectionLost(self, reason):
        self.helper().lostConnection(self.transport, reason)
        if self.transport in self.factory.all_transports:
            self.factory.all_transports.remove(self.transport)

class ServerHelper(object):
    def __init__(self):
        self.factory = None

    def init_factory(self, factory):
        self.factory = factory

    def kill_factory(self):
        self.factory = None

    def newConnection(self, transport):
        print "New Connection:", transport
        self.write(transport, "Welcome!")

    def lostConnection(self, transport, reason):
        print "Lost Connection:", transport, "reason:\n", reason

    def receiveData(self, transport, data):
        print "Received data from:", transport
        print ":->Data:", data
        self.write(transport, "!WeDidReceive: "+data)

    def killTransport(self, transport):
        transport.loseConnection()

    def write(self, transport, data):
        transport.write(safe_store.store(data)+END_LINE)

class ServerFactory(Factory):
    def __init__(self, helper, protocol, transport):
        self.helper = helper
        self.protocol = protocol
        self.transport = transport
        self.all_transports = []

    def startFactory(self):
        self.helper.init_factory(self)

    def stopFactory(self):
        self.helper.kill_factory()

class Server(object):
    def __init__(self, port=98765, helper=None, protocol=None,
                 transport=None):
        if not helper:
            helper = ServerHelper
        if not protocol:
            protocol = ServerProtocol
        if not transport:
            transport = ServerTransport
        self.helper = helper()
        self.factory = ServerFactory(self.helper, protocol, transport)

        self.port = port

    def run(self):
        reactor.listenTCP(self.port, self.factory)
        reactor.run()
