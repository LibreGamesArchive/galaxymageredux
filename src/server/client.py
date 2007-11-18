from twisted.spread import pb
from twisted.internet import reactor
from twisted.cred import credentials

class Client(pb.Referenceable):
    def __init__(self, hostname, port, username):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.avatar = None

    def connect(self):
        f = pb.PBClientFactory()
        reactor.connectTCP(self.hostname, self.port, f)
        cred = credentials.UsernamePassword(self.username, self.username)
        d = f.login(cred, self)
        d.addCallback(self.connected)
        d.addErrback(self.shutdown)
        reactor.run()
        
    def connected(self, avatar):
        print "connected..."
        self.avatar = avatar

    def shutdown(self, result):
        reactor.stop()

    def remote_serverMessage(self, message):
        print message

Client("localhost", 44444, "ajhager").connect()
