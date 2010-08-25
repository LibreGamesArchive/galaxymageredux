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
        master = self.players[0]
        self.talkToPlayer(master, 'youAreNowMaster', None)

    def get_master(self):
        return self.players[0]

    def add_player(self, avatar):
        avatar.game = self
        self.players.append(avatar)
        name = self.get_free_names()[0]
        self.picked_names.append(name)
        self.server.remote(avatar, 'joinedGame', self.scenario, name)
        #NOTE: this has to be a regular server call still!
        if self.is_master(avatar):
            self.make_master()

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

    def get_command(self, avatar, command, args):
        getattr(self, command)(avatar, args)

    def talkToPlayer(self, avatar, command, args):
        self.server.remote(avatar, 'getTalkFromServer', command, args)
