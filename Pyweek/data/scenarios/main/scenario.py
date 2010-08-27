

class Scenario(object):
    def initialize(self):
        #this is where we determine our own variables
        Unit('fighter', 'goodguys',
             ('Bob', (2,1), 1))
        print parent.units

store.scenario = Scenario()
