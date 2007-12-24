import battle
import unit
from map import Map, MapPanel

b = battle.Battle()
alice = unit.Unit( "Alice", unit.Gender.FEMALE )
alice.statistics[ unit.Statistic.SPEED ].base = 10
alice.statistics[ unit.Statistic.MOVEMENT_RANGE ].base = 2
bob = unit.Unit( "Bob", unit.Gender.MALE )
bob.statistics[ unit.Statistic.SPEED ].base = 7
b.clocktick += alice.update
b.clocktick += bob.update



m = Map(5, 5, 1)
alice.add_to_map(m, 0, 0, 0)