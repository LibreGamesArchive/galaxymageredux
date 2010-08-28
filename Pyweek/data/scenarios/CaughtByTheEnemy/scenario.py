

class Scenario(BaseScenario):
    def initialize(self):
        #this is where we determine our own variables
        # Good Guys Team
        Unit('fighter', 'goodguys',('Bob', (0,0), 1))
        Unit('fighter', 'goodguys',('Rob', (0,1), 1))
        Unit('fighter', 'goodguys',('Cob', (0,2), 1))
        Unit('archer', 'goodguys',('Sob', (1,1), 1))
        
        # Bad Guys Team
        Unit('fighter', 'badguys',('Guard', (4,13), 1))
        Unit('fighter', 'badguys',('Guard', (4,15), 1))
        Unit('fighter', 'badguys',('Guard', (6,14), 1))

        self.engine.setScenarioMess('Welcome', 'unit-test-fighter.gif')

    def winner(self):
        return None #none or team/player that won

    def closeScenarioMess(self):
        print 'closed :('

store.scenario = Scenario
