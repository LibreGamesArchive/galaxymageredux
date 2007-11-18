# LICENSE:
#
# Copyright (c) 2007 Brandon Barnes and GalaxyMage Redux contributors.
#
# GalaxyMage Redux is free software; you can redistribute it and/or 
# modify it under the terms of version 2 of the GNU General Public 
# License, as published by the Free Software Foundation.
# 
# GalaxyMage Redux is distributed in the hope that it will be useful, 
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with GalaxyMage Redux; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.

from zope.interface import implements

from twisted.spread import pb
from twisted.cred import checkers, portal, credentials
from twisted.internet import reactor, defer

class Server(object):
    def __init__(self):
        self.players = []

    def join(self, player):
        self.remoteAll("serverMessage", "%s joined the server" % player.name)
        self.players.append(player)

    def leave(self, player):
        self.players.remove(player)
        self.remoteAll("serverMessage", "%s left the server" % player.name)

    def remote(self, player, action, *args):
        df = player.client.callRemote(action, *args)
        return df

    def remoteAll(self, action, *args):
        dfs = []
        for player in self.players:
            dfs.append(self.remote(player, action, *args))
        return dfs

class Player(pb.Avatar):
    def __init__(self, name, server, clientRef):
        self.name = name
        self.server = server
        self.client = clientRef

    def attached(self):
        self.server.join(self)

    def detached(self):
        self.server.leave(self)
        self.server = None
        self.client = None

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
    def __init__(self, port):
        self.port = port
        self.server = Server()

    def start(self):
        c = UsernameChecker()
        p = portal.Portal(self)
        p.registerChecker(c)
        reactor.listenTCP(self.port, pb.PBServerFactory(p))
        reactor.run()

    def requestAvatar(self, name, clientRef, *interfaces):
        assert pb.IPerspective in interfaces
        avatar = Player(name, self.server, clientRef)
        avatar.attached()
        return pb.IPerspective, avatar, lambda a=avatar:a.detached()

Realm(44444).start()
