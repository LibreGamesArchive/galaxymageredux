import newnet

class PlayerAvatar(newnet.BaseAvatar):
    def perspective_sendMessage(self, message):
        self.server.PA_sendMessage(self, message)

class CreatorAvatar(newnet.BaseAvatar):
    def perspective_sendMessage(self, message):
        self.server.CA_sendMessage(self, message)

class GameServer(newnet.Server):
    def __init__(self):
        newnet.Server.__init__(self)
        self.users = 0

    def requestNewAvatar(self):
        self.users += 1
        if self.users == 1:
            return CreatorAvatar
        return PlayerAvatar

    def PA_sendMessage(self, avatar, message):
        self.remoteAll("GetMessage", "player", avatar.name, message)

    def CA_sendMessage(self, avatar, message):
        self.remoteAll("GetMessage", "creator", avatar.name, message)

##    def update(self):
##        print "update!"


s = GameServer()
r = newnet.Realm(44444, s)
r.start()
