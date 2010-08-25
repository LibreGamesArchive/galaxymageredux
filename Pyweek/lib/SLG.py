"""Server and client for the server-game-server"""


import net, urllib, time
from server_game_engine import Game

main_server_host = 'localhost' #change to real server later!
main_server_port = 54321

class Server(net.Server):
    def __init__(self):
        net.Server.__init__(self)

        self.games_list = {}

        self.last_push_update = time.time()
        self.push_update_delay = 5 #seconds

    def join(self, avatar):
        print avatar.name, 'joined'
        net.Server.join(self, avatar)
        self.remote(avatar, 'OverrideUsername', avatar.name)
        self.sendServerMessage('%s has joined the server'%avatar.name)

    def leave(self, avatar):
        print avatar.name, 'left'
        net.Server.leave(self, avatar)
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

    def makeGame(self, avatar, name, scenario, available_scenarios):
        if avatar.game:
            return
        new = Game(self, name, scenario)
        new_id = id(new)
        new.game_id = new_id
        self.games_list[new_id] = new

        new.add_player(avatar, available_scenarios)

    def update(self):
        #basically, every 15 seconds, make every client reget the server info to keep it updated...
        if time.time() - self.last_push_update > self.push_update_delay:
            for i in self.avatars:
                if not i.game:
                    self.getLobbyUsersList(i)
                    self.getGameList(i)
            self.last_push_update = time.time()

    def requestJoinGame(self, avatar, game_id, available_scenarios):
        game = self.games_list[game_id]
        if game.playing:
            self.remote(avatar, 'cannotJoinGame', 'ingame')
            return
        if len(game.players) >= game.max_players:
            self.remote(avatar, 'cannotJoinGame', 'full')
            return
        if not game.scenario in available_scenarios:
            self.remote(avatar, 'cannotJoinGame', 'scen')
            return

        game.add_player(avatar, available_scenarios)

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

    def talkToGame(self, avatar, command, args):
        if avatar.game:
            avatar.game.get_command(avatar, command, args)

class SLGAvatar(net.BaseAvatar):
    def __init__(self, name, server, clientRef):
        net.BaseAvatar.__init__(self, name, server, clientRef)
        self.game = None

    def perspective_getGameList(self):
        self.server.getGameList(self)

    def perspective_makeGame(self, name, scenario, a_scen):
        if not self.game:
            self.server.makeGame(self, name, scenario, a_scen)

    def perspective_requestJoinGame(self, game_id, a_scen):
        if not self.game:
            a = self.server.requestJoinGame(self, game_id, a_scen)

    def perspective_sendMessage(self, message):
        self.server.sendMessage(self, message)

    def perspective_talkToGame(self, command, args):
        self.server.talkToGame(self, command, args)

class Client(net.Client):
    def remote_sendGameList(self, games):
        pass
    def remote_getMessage(self, player, message):
        pass
    def remote_sendLobbyUsersList(self, users):
        pass
    def remote_getTalkFromServer(self, command, args):
        pass
    def remote_joinedGame(self, scenario, team):
        pass
    def remote_cannotJoinGame(self, reason):
        pass
