import battle
import unit
from map import Map, MapPanel

b = battle.Battle()
alice = unit.Unit( "Alice", unit.Gender.FEMALE, b )
alice.statistics[ unit.Statistic.SPEED ].base = 10
alice.statistics[ unit.Statistic.MOVE_RANGE ].base = 3
bob = unit.Unit( "Bob", unit.Gender.MALE, b )
bob.statistics[ unit.Statistic.SPEED ].base = 7


m = Map(5, 5, 1)
alice.add_to_map(m, 0, 0, 0)
