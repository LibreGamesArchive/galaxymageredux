""" Artificial Intelligence, implemented as a SLG.Client
    Initialize with the master of the game, the game itself and the scenario
    After initialized acts similarly to a player.
    Robert Ramsay
"""

from time import time
from lib import SLG, event, client_game_engine
from math import sqrt

class AI_Client(SLG.Client):
    def __init__(self, master, game, scenario, name = None):
        self.game = game
        self.scen = scenario
        if name == None or len(name) == 0:
            # Get a pseudo unique name in the case of 1+ bots and 0 creativity
            t = time()
            name = 'Robot' + str(int(t*1000) - int(t/10)*10000)
        SLG.Client.__init__(self, name, master.hostname, master.port)
        self.Connect()

    def update(self):
        if my_turn:
            for unit in my_team:
                closest_enemy = find_closest_enemy(unit, game)
                if unit.type == fighter:
                    unit.move(closest_enemy)
                    unit.attack(closest_enemy)
                if unit.type == archer:
                    unit.move_range_limit(closest_enemy)
                    unit.attack(closest_enemy)
                if unit.type == mage:
                    location = find_closest_injured(unit, 0.5, game)
                    if location:
                        unit.move_range_limit(location)
                        unit.heal(location)
                    else:
                        unit.move_range_limit(closest_enemy)
                        unit.attack(closest_enemy)

    def find_closest_enemy(unit, game):
        start = (unit.X, unit.Y)
        r = 1
        enemy = None
        map = game.map
        while not enemy and r < unit.range + unit.mv:
            potentials = list()
            for i in range(start.X-r,start.X+r):
                for j in range(start.Y-r,start.Y+r):
                    if map[i,j] is unit and
                       my_team.index(map[i,j]) == None and
                       map[i,j].hp > 0:
                        potentials.append(map[i,j])
            for e in potentials:
                if enemy:
                    if enemy.hp > e.hp: 
                        enemy = e
                else:
                    enemy = e
        return enemy

    def find_closest_injured(unit, threshold, game):
        r_max = unit.mv + unit.range
        r = r_max + 1
        patient = None
        for u in my_team:
            if u.hp < threshold:
                distance = sqrt((u.x-unit.x)**2+(u.y-unit.y)**2) # replace with some better graph search
                if distance < r:
                    if patient and patient.hp > u.hp:
                        pass
                    else:
                        patient = u
        return patient
