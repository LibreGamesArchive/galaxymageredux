class Game(object):
    def __init__(self, server, name, scenario):
        self.name = name
        self.server = server
        self.scenario = scenario
        self.game_id = None

        self.abs_max = 10 #no more players than that! Period!
        self.last_master = ""

        self.players = []
        self.player_scenarios = {}
        self.teams = []
        #TODO: build teams based on scenario, assign players to them in add_player
        self.max_players = 2
        self.scen_team_names = ['def1', 'def2']
        self.picked_names = {}

        self.playing = False

    def is_master(self, avatar):
        return avatar == self.players[0]

    def make_master(self):
        master = self.players[0]
        self.talkToPlayer(master, 'youAreNowMaster', None)
        self.server.update_game_settings(self)
        self.last_master = master

    def get_master(self):
        return self.players[0]

    def get_free_names(self):
        n = []
        pn = self.picked_names.values()
        for i in self.scen_team_names:
            if not i in pn:
                n.append(i)
        return n

    def get_player_names(self):
        return [i.name for i in self.players]

    def get_player_names_teams(self):
        l = []
        for i in self.players:
            l.append((i.name, self.picked_names[i]))
        return l

    def add_player(self, avatar, a_scen):
        avatar.game = self
        self.player_scenarios[avatar] = a_scen
        self.players.append(avatar)
        name = self.get_free_names()[0]
        self.picked_names[avatar] = name

        #NOTE: this has to be a regular server call still!
        self.server.remote(avatar, 'joinedGame', self.name, self.scenario, name)

        if self.is_master(avatar):
            self.make_master()
            print '%s made room <%s>'%(avatar.name, self.name)
        self.talkToAllPlayers('stillFreeTeamNames', self.get_free_names())
        self.talkToAllPlayers('playerNamesTeams', self.get_player_names_teams())
        self.talkToAllPlayers('getMessage', ('<server>', '%s joined the game'%avatar.name))
        self.server.update_game_settings(self)

    def player_leave(self, avatar):
        if avatar in self.players:
            master = self.get_master()
            self.players.remove(avatar)
            avatar.game = None
            del self.picked_names[avatar]
            if self.players == []:
                del self.server.games_list[self.game_id]
                print 'game room <%s> closed'%self.name
                self.server.gameClose(self)
                return
            else:
                if master == avatar:
                    self.make_master()
            self.talkToAllPlayers('stillFreeTeamNames', self.get_free_names())
            self.talkToAllPlayers('playerNamesTeams', self.get_player_names_teams())
            self.talkToAllPlayers('getMessage', ('<server>', '%s left the game'%avatar.name))
            self.server.update_game_settings(self)

    def getGameScenarioInfo(self, avatar, config):
        if self.is_master(avatar):
            self.scenario = config['name']
            self.max_players = config['maxp']
            self.scen_team_names = config['teams']
            self.picked_names = {}

            free_names = self.get_free_names()
            x = 0
            tobe_kicked = []
            for i in self.players:
                if not self.scenario in self.player_scenarios[i]:
                    self.talkToPlayer(i, 'kickedDueToScenario', None)
                    tobe_kicked.append(i)
                elif x > self.max_players:
                    self.talkToPlayer(i, 'kickedDueToTooManyPlayers', None)
                    tobe_kicked.append(i)
                else:
                    team = free_names.pop(0)
                    self.picked_names[i] = team
                    self.talkToPlayer(i, 'scenarioChanged', (self.scenario, team, self.max_players))
                x += 1

            for i in tobe_kicked:
                self.player_leave(i)
            self.talkToAllPlayers('playerNamesTeams', self.get_player_names_teams())
            if not tobe_kicked:
                self.talkToAllPlayers('stillFreeTeamNames', self.get_free_names())
        self.server.update_game_settings(self)

    def kickPlayer(self, avatar, name):
        if self.is_master(avatar):
            for i in self.players:
                if i.name == name:
                    self.talkToPlayer(i, 'kickedByMaster', None)
                    self.player_leave(i)
                    self.talkToAllPlayers('getMessage', ('<server>', '%s KICKED %s!!!'%(avatar.name, name)))
                    self.server.update_game_settings(self)
                    return

    def get_command(self, avatar, command, args):
        getattr(self, command)(avatar, args)

    def talkToPlayer(self, avatar, command, args):
        self.server.remote(avatar, 'getTalkFromServer', command, args)

    def talkToAllPlayers(self, command, args):
        for avatar in self.players:
            self.talkToPlayer(avatar, command, args)

    def player_message(self, avatar, message):
        self.talkToAllPlayers('getMessage', (avatar.name, message))

    def playerTeamChange(self, avatar, new):
        if new in self.get_free_names():
            self.picked_names[avatar] = new
            self.talkToAllPlayers('stillFreeTeamNames', self.get_free_names())
            self.talkToAllPlayers('playerNamesTeams', self.get_player_names_teams())
