from twisted.internet.protocol import Protocol

from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor

class ServerProtocol(Protocol):
    def helper(self):
        return self.factory.helper

    def connectionMade(self):
        self.helper().newConnection(self.transport)

    def dataReceived(self, data):
        self.helper().receiveData(self.transport, data)

    def connectionLost(self, reason):
        self.helper().lostConnection(self.transport, reason)

class ServerHelper(object):
    def __init__(self):
        self.factory = None

    def init_factory(self, factory):
        self.factory = factory

    def kill_factory(self):
        self.factory = None

    def newConnection(self, transport):
        print "New Connection:", transport
        transport.write("Welcome!")

    def lostConnection(self, transport, reason):
        print "Lost Connection:", transport, "reason:\n", reason

    def receiveData(self, transport, data):
        print "Received data from:", transport
        print ":->Data:", data
        transport.write(["Received", data])

    def killTransport(self, transport):
        transport.loseConnection()

class ServerFactory(Factory):
    def __init__(self, helper, protocol):
        self.helper = helper
        self.protocol = protocol

    def startFactory(self):
        self.helper.init_factory(self)

    def stopFactory(self):
        self.helper.kill_factory()

class Server(object):
    def __init__(self, port=98765, helper=None, protocol=None):
        if not helper:
            helper = ServerHelper
        if not protocol:
            protocol = ServerProtocol
        self.helper = helper()
        self.factory = ServerFactory(self.helper, protocol)

        self.port = port

    def run(self):
        reactor.listenTCP(self.port, self.factory)
        reactor.run()
