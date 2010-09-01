

class Unit(BaseUnit):
    type = 'archer'
    def initialize(self):
        self.strength = 4
        self.hp = 5
        self.boost_hp = 2
        self.boost_strength = 1
        self.action_points = 6
        self.image = 'unit-test-archer.gif'

        self.have_ability('move')
        self.have_ability('bow_attack')

        self.desc = 'A long range fighter'

store.unit = Unit
