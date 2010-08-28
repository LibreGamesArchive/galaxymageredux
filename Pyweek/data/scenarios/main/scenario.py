

class Scenario(BaseScenario):
    def initialize(self):
        #this is where we determine our own variables
        # Good Guys Team
        Unit('fighter', 'goodguys',('Bob', (0,0), 1))
        Unit('fighter', 'goodguys',('Rob', (0,1), 1))
        Unit('fighter', 'goodguys',('Cob', (0,2), 1))
        
        # Bad Guys Team
        Unit('fighter', 'badguys',('Felix', (4,0), 1))
        Unit('fighter', 'badguys',('Frank', (4,1), 1))
        Unit('fighter', 'badguys',('Fritz', (4,2), 1))

        self.engine.setScenarioMess('Welcome', 'unit-test-fighter.gif')

    def winner(self):
        return None #none or team/player that won

    def closeScenarioMess(self):
        print 'closed :('

store.scenario = Scenario
