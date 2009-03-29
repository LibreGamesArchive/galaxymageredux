from twisted.spread import pb
from twisted.internet import reactor, defer, threads
from twisted.cred import checkers, portal, credentials

from zope.interface import implements

#high level stuff we shouldn't have to deal with further...

class UsernameChecker(object):
    implements(checkers.ICredentialsChecker)
    credentialInterfaces = (credentials.IUsernamePassword,
                            credentials.IUsernameHashedPassword)

    def __init__(self):
        self.usernames = []

    def requestAvatarId(self, cred):
        username = cred.username
        if username in self.usernames:
            num = 1
            while username+str(num) in self.usernames:
                num += 1
            username += str(num)
        self.usernames.append(username)
        return defer.succeed(username)

class Realm(object):
    implements(portal.IRealm)
    def __init__(self, port, server):
        self.port = port
        self.server = server

    def start(self):
        c = UsernameChecker()
        p = portal.Portal(self)
        p.registerChecker(c)
        reactor.listenTCP(self.port, pb.PBServerFactory(p))
        self.server.run_updater()
        reactor.run()

    def requestAvatar(self, name, clientRef, *interfaces):
        assert pb.IPerspective in interfaces

        avatarType = self.server.requestNewAvatar()

        avatar = avatarType(name, self.server, clientRef)
        avatar.attached()

        return pb.IPerspective, avatar, lambda a=avatar:a.detached()

##########Server stuff!

class Server(object):
    def __init__(self):
        self.avatarTypes = {}
        self.avatars = []
        self.type = ''
        self.running = True

        self.users = 0

    def join(self, avatar):
        self.avatars.append(avatar)
        self.remoteAll("getMessage", "%s joined the server" % avatar.name)

    def leave(self, avatar):
        self.avatars.remove(avatar)
        self.remoteAll("getMessage", "%s left the server" % avatar.name)

    def remote(self, avatar, action, *args):
        df = avatar.client.callRemote(action, *args)
        return df

    def remoteAll(self, action, *args):
        dfs = []
        for avatar in self.avatars:
            try:
                dfs.append(self.remote(avatar, action, *args))
            except:
                pass
        return dfs

    def requestNewAvatar(self):
        self.users += 1
        if self.users == 1:
            return CreatorAvatar
        return PlayerAvatar

    def run_updater(self):
        self.update()
        if self.running:
            reactor.callLater(0, self.run_updater)

    def update(self):
        pass

    def PA_sendMessage(self, avatar, message):
        #server methods that are available do NOT have to be preceeded with eithe rremote_ or perspective_
        self.remoteAll("getMessage", "player: " + avatar.name + ": " + message)

    def CA_sendMessage(self, avatar, message):
        self.remoteAll("getMessage", "creator: " + avatar.name + ": " + message)

    def start(self, port):
        self.realm = Realm(port, self)
        self.realm.start()


#########Client stuff!

class BaseAvatar(pb.Avatar):
    #the avatar is given to each client, and the kind given indicates the amount of access the client has
    #this object is used to contact the server and send a request
    def __init__(self, name, server, clientRef):
        self.name = name
        self.server = server
        self.client= clientRef

    def attached(self):
        self.server.join(self)

    def detached(self):
        self.server.leave(self)
        self.server = None
        self.client = None

class PlayerAvatar(BaseAvatar):
    def perspective_sendMessage(self, message):
        self.server.PA_sendMessage(self, message)

class CreatorAvatar(BaseAvatar):
    def perspective_sendMessage(self, message):
        self.server.CA_sendMessage(self, message)


class Client(pb.Referenceable):
    #the client is the low level connection class - anything we want the server to be able to contact needs to be here.
    #we contact the server through this client by accessing our avatar:
    #self.avatar.callRemote("Name", *args, **kwargs) - where "Name" is the method
    #   name from the avatar, preceeded by "perspective_" - so "perspective_Name"
    #a method that is accessible by the server is preceeded with the "remote_" name
    def __init__(self, hostname, port, username):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.avatar = None

        self._connected = False
        self.running = True

        self.run_updater()
        reactor.run()

        self.connection = None

    def connect(self):
        f = pb.PBClientFactory()
        self.connection = reactor.connectTCP(self.hostname, self.port, f)
        cred = credentials.UsernamePassword(self.username, self.username)
        d = f.login(cred, self)
        d.addCallback(self.connected)
        d.addErrback(self.errHandler)

    def disconnect(self):
        if self.connection:
            self.connection.disconnect()
            self.connection = None
        
    def connected(self, avatar):
        self.avatar = avatar
        self._connected = True

    def run_updater(self):
        self.update()
        if self.running:
            reactor.callLater(0, self.run_updater)

    def update(self):
        pass

    def shutdown(self, result):
        print result
        self._connected = False
        self.running = False
        reactor.stop()

    def errHandler(self, result):
        print result

    def close(self):
        reactor.stop()
        self.running = False
        self._connected = False

    # Methods callable by the server
    def remote_getMessage(self, message):
        print 'Got "', message, '" from server'
