# LICENSE:
#
# Copyright (c) 2007-2008 A. Joseph Hager and Redux contributors.
#
# Redux is free software; you can redistribute it and/or modify it under the
# terms of version 2 of the GNU General Public License, as published by the
# Free Software Foundation.
# 
# Redux is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
# 
# You should have received a copy of the GNU General Public License along
# with Redux; if not, write to the Free Software Foundation, Inc., 51 Franklin
# Street, Fifth Floor, Boston, MA 02110-1301, USA.


from zope.interface import implements
from twisted.spread import pb
from twisted.cred import checkers, portal, credentials
from twisted.internet import reactor, defer


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
        #reactor.run()

    def requestAvatar(self, name, clientRef, *interfaces):
        assert pb.IPerspective in interfaces

        # TODO: Make a proper way to hand out the right avatar
        if self.server.type == 'game':
            avatarType = self.server.avatarTypes["creator"]
        elif self.server.avatars == []:
            avatarType = self.server.avatarTypes["creator"]
        else:
            avatarType = self.server.avatarTypes["collaborator"]

        avatar = avatarType(name, self.server, clientRef)
        avatar.attached()

        return pb.IPerspective, avatar, lambda a=avatar:a.detached()
