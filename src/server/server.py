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
from twisted.cred import checkers, portal
from twisted.internet import reactor

class Server:
    def __init__(self):
        self.games = {}
    def joinGame(self, gamename, player):
        if not self.games.has_key(gamename):
            self.games[gamename] = Game(gamename)
        self.games[gamename].addPlayer(player)
        return self.games[gamename]

class Player(pb.Avatar):
    def __init__(self, name, server, clientRef):
        self.name = name
        self.server = server
        self.remote = clientRef
    def detached(self, clientRef):
        self.remote = None
    def perspective_joinGame(self, gamename):
        return self.server.joinGame(gamename, self)
    def send(self, message):
        self.remote.callRemote("print", message)

class Realm:
    implements(portal.IRealm)
    def __init__(self, port):
        self.port = port
        self.server = Server()

    def start(self):
        c = checkers.InMemoryUsernamePasswordDatabaseDontUse(ajhager="ajhager",markus="markus")
        p = portal.Portal(self)
        p.registerChecker(c)
        reactor.listenTCP(self.port, pb.PBServerFactory(p))
        reactor.run()

    def requestAvatar(self, name, clientRef, *interfaces):
        assert pb.IPerspective in interfaces
        avatar = Player(name, self.server, clientRef)
        return pb.IPerspective, avatar, lambda a=avatar:a.detached(clientRef)

class Game(pb.Viewable):
    def __init__(self, gamename):
        self.name = gamename
        self.players = []
    def addPlayer(self, player):
        self.players.append(player)
    def view_send(self, from_player, message):
        for player in self.players:
            print player.name
            player.send("<%s>: %s" % (from_player.name, message))
        return self

Realm(44444).start()
