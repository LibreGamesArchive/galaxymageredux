

class Scenario(object):
    def initialize(self):
        #this is where we determine our own variables
        Unit('fighter', 'goodguys', ('Bob', (0.5,0.5), 1))
        print parent.units

store.scenario = Scenario()
