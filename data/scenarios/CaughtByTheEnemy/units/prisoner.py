

class Unit(BaseUnit):
    type = 'prisoner'
    def initialize(self):
        self.strength = 10
        self.hp = 20
        self.boost_hp = 5
        self.boost_strength = 2
        self.action_points = 4
        self.image = 'unit-test-prisoner.gif'

##        self.have_ability('move')

        self.desc = 'Your leader - rescue him!'

store.unit = Unit
