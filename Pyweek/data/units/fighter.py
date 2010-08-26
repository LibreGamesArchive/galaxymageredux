

class Unit(BaseUnit):
    type = 'fighter'
    def __init__(self):
        BaseUnit.__init__(self)

        self.stats = {'strength':10,
                      "health":10,
                      'agility':10}

store.unit = Unit
