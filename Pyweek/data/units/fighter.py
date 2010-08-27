

class Unit(BaseUnit):
    type = 'fighter'
    def initialize(self):
        self.base_stats = {'strength':10,
                           "health":10,
                           'agility':10}
        self.image = 'test-ent1.gif'
        print self.abilities
        self.actions = {'walk': self.abilities['move'](self)}

store.unit = Unit
