""" Artificial Intelligence
    Really just a static class with some public decision-making methods.
    1. Could be overloaded in the future to give decisions attributes like:
       aggression or survivalism.
    Robert Ramsay
"""

from math import sqrt

class AI_Player:
    def update(self,
               gamestate, # Current status of game: map, units, locations
               gameactions, # The class that has the methods the AI must call
               my_team # Sequence of units that make up this time. Might be 
                       #  good enough to just give the team name and get the
                       #  units from teh gamestate.
               ):
        for unit in my_team:
            closest_enemy = find_closest_enemy(unit, gamestate.map)
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

    def find_closest_enemy(unit, map):
        x = unit.X
        y = unit.Y
        r = 1
        enemy = None
        while not enemy and r < unit.range + unit.mv:
            potentials = list()
            for i in range(x-r,x+r):
                for j in range(y-r, y+r):
                    if map[i][j] is unit and my_team.index(map[i][j]) == None and map[i][j].hp > 0:
                        potentials.append(map[i][j])
            for e in potentials:
                if enemy:
                    if enemy.hp > e.hp: 
                        enemy = e
                else:
                    enemy = e
            r += 1
        return enemy

    def find_closest_injured(unit, game, threshold = 0.5,):
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
