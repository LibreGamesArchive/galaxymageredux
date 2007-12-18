from Battle import *
from Unit import *

b = Battle()
alice = Unit("Alice", "FEMALE")
alice.Statistics[ "Speed" ].Base = 10
bob = Unit("Bob", "MALE")
bob.Statistics[ "Speed" ].Base = 7
b.Clocktick += alice.Update
b.Clocktick += bob.Update
b.DoBattle()

