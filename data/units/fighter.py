

class Unit(BaseUnit):
    type = 'fighter'
    def initialize(self):
        self.strength = 10
        self.hp = 10
        self.boost_hp = 5
        self.boost_strength = 2
        self.action_points = 5
        self.image = 'unit-test-fighter.gif'

        self.have_ability('move')
        self.have_ability('sword_attack')

        self.desc = 'A typical fighter unit'

store.unit = Unit
