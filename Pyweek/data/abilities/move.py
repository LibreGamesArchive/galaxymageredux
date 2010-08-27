

class Ability(BaseAbility):
    def initialize(self):
        self.cost = 1

    def test_available(self):
        mapd = self.unit.scenario.engine.gfx.mapd #yikes!
        if self.unit.cur_ap >= 2: #can't be last action!
            return True

store.ability = Ability
