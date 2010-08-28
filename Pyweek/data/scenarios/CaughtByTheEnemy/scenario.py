

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

        self.max_turns = 20
        self.turn = 1
        self.last_turn = 'goodguys'
        self.label = gui.Label(self.engine.engine.app,
                               (500, 5),
                               'Turn: 1/20')
        self.label.text_color = (255,255,255)

    def winner(self):
        if self.turn > self.max_turns:
            return 'badguys'

        fine = False
        for i in self.engine.units:
            if i.team == 'goodguys':
                if i.dead == False:
                    fine = True
                    break

        if not fine:
            return 'badguys'
        return None #none or team/player that won

    def closeScenarioMess(self):
        print 'closed :('

    def update(self):
        whos_turn = self.engine.engine.engine.whos_turn #OMG yuck!
        self.label.text = 'Turn: %s/20'%self.turn
        if not whos_turn == self.last_turn:
            if whos_turn == 'goodguys':
                self.turn += 1
            self.last_turn = whos_turn

store.scenario = Scenario
