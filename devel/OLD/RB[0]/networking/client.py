from twisted.internet import reactor
import twisted.internet.protocol as tprotocol

class ClientProtocol(tprotocol.Protocol):
    def __init__(self, factory):
        self.factory = factory

    def dataReceived(self, data):
        self.factory.helper.receiveData(self.transport, data)

    def connectionMade(self):
        self.factory.transport = self.transport

    def connectionLost(self, reason):
        self.factory.helper.lostConnection(self.transport, reason)
        self.factory.transport = None

class ClientHelper(object):
    def __init__(self):
        self.factory = None

    def init_factory(self, factory):
        self.factory = factory

    def dispatch(self, data):
        if self.factory.transport:
            self.factory.transport.write(data)
        else:
            print "TError!"

    def receiveData(self, transport, data):
        print "Received data from: server"
        print ":->Data:", data

    def lostConnection(self, transport, reason):
        print "Connection lost, reason:\n", reason

class ClientFactory(tprotocol.ClientFactory):
    def __init__(self, helper, protocol):
        self.helper = helper
        self.protocol = protocol
        self.transport = None
        self.helper.init_factory(self)

    def buildProtocol(self, addr):
        return self.protocol(self)

    def clientConnectLost(self, connector, reason):
        self.helper.lostConnection(connector, reason)

class Client(object):
    def __init__(self, app, port=98765, hostname="localhost",
                 helper=None, protocol=None):
        if not helper:
            helper = ClientHelper
        if not protocol:
            protocol = ClientProtocol

        self.helper = helper()
        self.factory = ClientFactory(self.helper, protocol)

        self.port = port
        self.hostname = hostname

        self.app = app(self)

    def run_app(self):
        self.app.loop()
        if self.app.is_running():
            reactor.callLater(0, self.run_app)

    def connect(self):
        reactor.connectTCP(self.hostname, self.port, self.factory)
        reactor.callLater(1, self.run_app)
        reactor.run()
