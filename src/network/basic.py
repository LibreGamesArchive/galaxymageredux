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

from twisted.spread import pb
from twisted.internet import reactor
from twisted.cred import credentials


class Server(object):
    def __init__(self):
        self.avatarTypes = {"creator" : CreatorAvatar,
                            "collaborator" : CollaboratorAvatar,
                            "observer" : ObserverAvatar,
                            "player" : PlayerAvatar}
        self.avatars = []
        self.type = ''

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


class CreatorAvatar(pb.Avatar):
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

class CollaboratorAvatar(pb.Avatar):
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

class ObserverAvatar(pb.Avatar):
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

class PlayerAvatar(pb.Avatar):
    """This class defines what a player's client can and cannot do on the 
    server. Any method prefixed with 'perspective_' may be invoked by the 
    client. This is only security level and the results of any call are dealt
    with by the game engine itself."""
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

    def perspective_requestMove(self, unit_id, position):
        # forward request to game engine with 'self' to ID the origin of the call
        self.server.requestMove(self, unit_id, position)

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
        self.update()

    def update(self):
        pass

    def shutdown(self, result):
        print result
        reactor.stop()
