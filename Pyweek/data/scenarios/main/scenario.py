

class Scenario(BaseScenario):
    def initialize(self):
        #this is where we determine our own variables
        Unit('fighter', 'goodguys',
             ('Bob', (2,1), 1))
        print parent.units

    def winner(self):
        return None #none or team/player that won

store.scenario = Scenario
