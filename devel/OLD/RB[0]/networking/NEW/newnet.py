

from twisted.spread import pb
from twisted.internet import reactor, defer
from twisted.cred import checkers, portal, credentials

from zope.interface import implements


class Server(object):
    def __init__(self):
        self.avatarTypes = {}
        self.avatars = []
        self.type = ''
        self.running = True

    def join(self, avatar):
        self.remoteAll("serverMessage", "%s joined the server" % avatar.name)
        self.avatars.append(avatar)

    def leave(self, avatar):
        self.avatars.remove(avatar)
        self.remoteAll("serverMessage", "%s left the server" % avatar.name)

    def remote(self, avatar, action, *args):
        df = avatar.client.callRemote(action, *args)
        return df

    def remoteAll(self, action, *args):
        dfs = []
        for avatar in self.avatars:
            dfs.append(self.remote(avatar, action, *args))
        return dfs

    def requestNewAvatar(self):
        return BaseAvatar

    def run_updater(self):
        self.update()
        if self.running:
            reactor.callLater(0, self.run_updater)

    def update(self):
        pass

class BaseAvatar(pb.Avatar):
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

class Client(pb.Referenceable):
    def __init__(self, hostname, port, username):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.avatar = None

        self.running = True

    def connect(self):
        f = pb.PBClientFactory()
        reactor.connectTCP(self.hostname, self.port, f)
        cred = credentials.UsernamePassword(self.username, self.username)
        d = f.login(cred, self)
        d.addCallback(self.connected)
        d.addErrback(self.shutdown)
        reactor.run()
        
    def connected(self, avatar):
        self.avatar = avatar
        self.running = True
        self.run_updater()

    def run_updater(self):
        self.update()
        if self.running:
            reactor.callLater(0, self.run_updater)

    def update(self):
        pass

    def shutdown(self, result):
        print result
        reactor.stop()

    def close(self):
        reactor.stop()
        self.running = False

    # Methods callable by the server
    def remote_getMessage(self, message):
        print 'Got "', message, '" from server'

class UsernameChecker(object):
    implements(checkers.ICredentialsChecker)
    credentialInterfaces = (credentials.IUsernamePassword,
                            credentials.IUsernameHashedPassword)

    def __init__(self):
        self.usernames = []

    def requestAvatarId(self, cred):
        username = cred.username
        while username in self.usernames:
            username = username + "_"
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
