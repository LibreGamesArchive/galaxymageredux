
class AI(BaseAI):
    def initialize(self):
        pass

    def update(self):
        enemy_list = []
        team_list = []
        # I think we need an AIHandler
        for u in self.scenario.units:
            if u.team == self.team:
                team_list.append(u)
            elif not u.dead:
                enemy_list.append(u)
        
        team_list[0].actions[0].perform((team_list[0].pos[0] -1, 
                                         team_list[0].pos[1]))
        self.scenario.engine.endMyTurn()
        self.scenario.engine.engine.sendMessage('<AI> I end turn')

store.ai = AI
