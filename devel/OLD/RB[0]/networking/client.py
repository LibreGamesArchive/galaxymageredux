from twisted.internet import reactor
import twisted.internet.protocol as tprotocol

class ClientProtocol(tprotocol.Protocol):
    def __init__(self, factory):
        self.factory = factory

    def sendData(self, data):
        self.transport.write(data)

    def dataReceived(self, data):
        self.factory.helper.receiveData(self.transport, data)

class ClientHelper(object):
    def __init__(self):
        self.factory = None

    def init_factory(self, factory):
        self.factory = factory

    def dispatch(self, data):
        self.factory.protocol.sendData(data)

    def receiveData(self, transport, data):
        print "Received data from: server"
        print ":->Data:", data

    def lostConnection(self, transport, reason):
        print "Connection lost, reason:\n", reason

class ClientFactory(tprotocol.ClientFactory):
    def __init__(self, helper, protocol):
        self.helper = helper
        self.protocol = protocol
        self.helper.init_factory(self)

    def buildProtocol(self, addr):
        return self.protocol(self)

    def clientConnectLost(self, connector, reason):
        self.helper.lostConnection(connector, reason)

class Client(object):
    def __init__(self, port=98765, hostname="localhost",
                 helper=None, protocol=None):
        if not helper:
            helper = ClientHelper
        if not protocol:
            protocol = ClientProtocol

        self.helper = helper()
        self.factory = ClientFactory(self.helper, protocol)

        self.port = port
        self.hostname = hostname

    def connect(self):
        reactor.connectTCP(self.hostname, self.port, self.factory)
        reactor.run()
