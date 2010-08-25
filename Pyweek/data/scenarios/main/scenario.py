

class Scenario(GameScenario):
    def initialize(self):
        #this is where we determine our own variables
        Unit('name',
             'team',
             'name',
             pos=(0,0),
             level=1)
