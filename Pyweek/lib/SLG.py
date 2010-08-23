"""Server and client for the server-game-server"""


import net, urllib

main_server_host = 'localhost' #change to real server later!
main_server_port = 54321

class Game(object):
    def __init__(self, server, name, scenario):
        self.name = name
        self.server = server
        self.scenario = scenario
        self.game_id = None

        self.players = []
        self.teams = []
        #TODO: build teams based on scenario, assign players to them in add_player
        self.max_players = 2

        self.playing = False

    def is_owner(self, avatar):
        return avatar == self.players[0]

    def get_master(self):
        return self.players[0]

    def add_player(self, avatar):
        self.players.append(avatar)

class DummyGame(object):
    def __init__(self, name):
        self.name = name
        self.scenario = "test"
        self.game_id = id(self)

        self.players = [DummyPlayer()]
        self.teams = []
        #TODO: build teams based on scenario, assign players to them in add_player
        self.max_players = 2

        self.playing = False

    def is_owner(self, avatar):
        return avatar == self.players[0]

    def get_master(self):
        return self.players[0]

    def add_player(self, avatar):
        self.players.append(avatar)

class DummyPlayer(object):
    def __init__(self):
        self.name = "testmaster"

class Server(net.Server):
    def __init__(self):
        net.Server.__init__(self)

        self.games_list = {}

        for i in xrange(10):
            self.games_list['test'+str(i)] = DummyGame('test'+str(i))

    def join(self, avatar):
        self.avatars.append(avatar)

    def leave(self, avatar):
        self.avatars.remove(avatar)
        if avatar.game:
            if avatar.game.is_owner(avatar):
                #set next player to owner!
                pass
            avatar.game.players.remove(avatar)
            if avatar.game.players == []:
                del self.games_list[avatar.game]

    def requestNewAvatar(self):
        return SLGAvatar

    def getGameList(self, avatar):
        games = []
        for i in self.games_list.values():
            games.append((i.game_id, i.name, i.scenario,
                          i.get_master().name,
                          len(i.players), i.max_players,
                          i.playing))
        self.remote(avatar, 'sendGameList', games)

    def makeGame(self, avatar, name, scenario):
        new = Game(self, name, scenario)
        new_id = id(new)
        new.game_id = new_id
        self.games_list[new_id] = new

        new.players.append(avatar)
        avatar.game = new

    def joinGame(self, avatar, game_id):
        game = self.games_list[game_id]
        if game.playing:
            return False
        if len(game.players) >= game.max_players:
            return False
        if not game.scenario in avatar.available_scenarios:
            return False

        game.add_player(avatar)
        return True

class SLGAvatar(net.BaseAvatar):
    def __init__(self, name, server, clientRef):
        net.BaseAvatar.__init__(self, name, server, clientRef)
        self.game = None
        self.available_scenarios = ['test'] #TODO: load from scenarios dir

    def perspective_getGameList(self):
        self.server.getGameList(self)

    def perspective_makeGame(self, name, scenario):
        if not self.game:
            self.server.makeGame(self, name, scenario)

    def perspective_joinGame(self, game_id):
        if not self.game:
            a = self.server.joinGame(self, game_id)
            print a, a.__dict__

class Client(net.Client):
    def remote_sendGameList(self, games):
        pass
