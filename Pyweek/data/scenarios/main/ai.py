
class AI(BaseAI):
    def initialize(self):
        pass

    def update(self):
        self.scenario.engine.endMyTurn()
        self.scenario.engine.engine.sendMessage('<AI> I end turn')

store.ai = AI
