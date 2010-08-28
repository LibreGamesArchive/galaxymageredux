

class Unit(BaseUnit):
    type = 'fighter'
    def initialize(self):
        self.strength = 10
        self.hp = 10
        self.action_points = 3
        self.image = 'unit-test-fighter.gif'
        print self.abilities
        self.actions = {'walk': self.abilities['move'](self)}

        self.desc = 'A typical fighter unit'

store.unit = Unit
