"""Server and client for the server-game-server"""


import net, urllib, time

main_server_host = 'localhost' #change to real server later!
main_server_port = 54321

class Game(object):
    def __init__(self, server, name, scenario):
        self.name = name
        self.server = server
        self.scenario = scenario
        self.game_id = None

        self.abs_max = 10 #no more players than that! Period!

        self.players = []
        self.teams = []
        #TODO: build teams based on scenario, assign players to them in add_player
        self.max_players = 2
        self.scen_team_names = ['def1', 'def2']
        self.picked_names = []

        self.playing = False

    def is_master(self, avatar):
        return avatar == self.players[0]

    def make_master(self):
        owner = self.players[0]
        self.server.remote(owner, 'youAreNowMaster')

    def get_master(self):
        return self.players[0]

    def add_player(self, avatar):
        avatar.game = self
        self.players.append(avatar)
        if self.is_master(avatar):
            self.make_master()
        name = self.get_free_names()[0]
        self.picked_names.append(name)
        self.server.remote(avatar, 'joinedGame', self.scenario, name)

    def set_scen_data(self, name, maxp, teams):
        self.scenario = name
        self.max_players = maxp
        self.scen_team_names = teams
        self.picked_names = []

        #todo: inform players of new scenario
        #todo: assign team names
        #todo: if too many players, kick oldest

    def get_free_names(self):
        n = []
        for i in self.scen_team_names:
            if not i in self.picked_names:
                n.append(i)
        return n

    def player_leave(self, avatar):
        master = self.get_master()
        self.players.remove(avatar)
        if self.players == []:
            del self.server.games_list[self.game_id]
        else:
            if master == avatar:
                self.make_master()

    def getGameScenarioInfo(self, avatar, config):
        if self.is_master(avatar):
            self.set_scen_data(config['name'], config['maxp'], config['teams'])

class Server(net.Server):
    def __init__(self):
        net.Server.__init__(self)

        self.games_list = {}

        self.last_push_update = time.time()
        self.push_update_delay = 5 #seconds

    def join(self, avatar):
        self.avatars.append(avatar)
        self.sendServerMessage('%s has joined the server'%avatar.name)

    def leave(self, avatar):
        self.avatars.remove(avatar)
        if avatar.game:
            avatar.game.player_leave(avatar)
        else:
            self.sendServerMessage('%s has left the server'%avatar.name)

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
        if avatar.game:
            return
        new = Game(self, name, scenario)
        new_id = id(new)
        new.game_id = new_id
        self.games_list[new_id] = new

        new.add_player(avatar)

    def update(self):
        #basically, every 15 seconds, make every client reget the server info to keep it updated...
        if time.time() - self.last_push_update > self.push_update_delay:
            for i in self.avatars:
                if not i.game:
                    self.getLobbyUsersList(i)
                    self.getGameList(i)
            self.last_push_update = time.time()

    def requestJoinGame(self, avatar, game_id):
        game = self.games_list[game_id]
        if game.playing:
            self.remote(avatar, 'cannotJoinGame')
        if len(game.players) >= game.max_players:
            self.remote(avatar, 'cannotJoinGame')
        if not game.scenario in avatar.available_scenarios:
            self.remote(avatar, 'cannotJoinGame')

        game.add_player(avatar)
        self.remote(avatar, 'joinedGame')

    def sendMessage(self, avatar, message):
        if avatar.game:
            pass #send to people in game room!
        else:
            for av in self.avatars:
                if not av.game:
                    self.remote(av, "getMessage", avatar.name, message)

    def sendServerMessage(self, message):
        for av in self.avatars:
            if not av.game:
                self.remote(av, "getMessage", '<server>', message)

    def getLobbyUsersList(self, avatar):
        users = []
        for i in self.avatars:
            if not i.game:
                users.append(i.name)
        self.remote(avatar, 'sendLobbyUsersList', users)

    def silentHandleFail(self, result):
        if 'twisted.spread.pb.PBConnectionLost' in result.parents:
            pass
        else:
            print result

    def remote(self, avatar, action, *args):
        d = avatar.client.callRemote(action, *args)
        d.addErrback(self.silentHandleFail)

    def getGameScenarioInfo(self, avatar, data):
        if avatar.game:
            avatar.game.getGameScenarioInfo(avatar, data)

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

    def perspective_sendMessage(self, message):
        self.server.sendMessage(self, message)

    def perspective_getGameScenarioInfo(self, config):
        self.server.getGameScenarioInfo(self, config)

class Client(net.Client):
    def remote_sendGameList(self, games):
        pass
    def remote_getMessage(self, player, message):
        pass
    def remote_sendLobbyUsersList(self, users):
        pass
    def remote_joinedGame(self, scenario, team):
        pass
    def remote_youAreNowMaster(self):
        pass
