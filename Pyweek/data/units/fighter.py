

class Unit(BaseUnit):
    type = 'fighter'
    def __init__(self):
        BaseUnit.__init__(self)

        self.base_stats = {'strength':10,
                           "health":10,
                           'agility':10}
        self.image = 'test-ent1.gif'

store.unit = Unit
