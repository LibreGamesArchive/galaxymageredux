from twisted.spread import pb
from twisted.internet import reactor
from twisted.cred import credentials

class Client(pb.Referenceable):
    def remote_print(self, message):
        print message

    def connect(self):
        f = pb.PBClientFactory()
        reactor.connectTCP("localhost", 44444, f)
        user = raw_input("Username: ")
        d = f.login(credentials.UsernamePassword(user, user), client=self)
        d.addCallback(self.connected)
        reactor.run()
        
    def connected(self, perspective):
        print "connected..."
        gamename = raw_input("Game: ")
        print "joining game " + gamename
        d = perspective.callRemote("joinGame", gamename)
        d.addCallback(self.gotGame)
   
    def gotGame(self, game):
        message = raw_input("Message: ")
        d = game.callRemote("send", message)
        if message == "q":
            d.addCallback(self.shutdown)
        else:
            d.addCallback(self.gotGame)

    def shutdown(self, result):
        reactor.stop()

Client().connect()
