""" Artificial Intelligence
    Really just a static class with some public decision-making methods.
    1. Could be overloaded in the future to give decisions attributes like:
       aggression or survivalism.
    Robert Ramsay
"""
from mod_base import BaseUnit
from math import sqrt
from sys import maxint

class AI_Player:
    def update(self,
               gamestate, # Current status of game: map, units, locations
               gameactions, # The class that has the methods the AI must call
               my_team # Sequence of units that make up this time. Might be 
                       #  good enough to just give the team name and get the
                       #  units from teh gamestate.
               ):
        for unit in my_team:
            closest_enemy = find_closest_enemy(unit, eng.mapd)
            move_along_path(unit, closest_enemy, eng.mapd)
            unit.attack(closest_enemy)

    def ValidSquare(x, y, map):
        ''' This will be replaced with a real check later, either here or by
        a method in MapHandler.
        Check for:
            Blocking Entities/Walls
            Point off map
            Distance not jumpable by unit
        '''
        return True

    def move_along_path(center, target, map, radius):
        ''' Makes best attempt to find a legal path to location and then move
        unit.'''
        if center is BaseUnit:
            x, y = center.pos
        else:
            x, y = center # Center is a tuple
        x = float(x)
        y = float(y)
        
        if target is BaseUnit:
            goal = (float(target.pos[0]), float(target.pos[1]))
        else:
            goal = (float(target[0]), float(target[1])) # target is a tuple

        for i in range(1,radius):
            d = sqrt((goal[0]-x)**2 + (goal[1]-y)**2)
            vector = ((goal[0]-x)/d,
                      (goal[1]-y)/d)
            if ValidSquare(x+int(vector[0]), y + int(vector[1]), map):
                x += int(vector[0])
                y += int(vector[1])
            else:
                pass

    def find_closest_enemy(center, map, radius = None):
        '''Searches until it finds an enemy. center may be the Unit searching
        for an enemy or a (col, row) tuple. radius limits how far from the
        center we can look.'''
        if center is BaseUnit:
            x, y = center.pos
        else:
            x, y = center # Center is a tuple
        
        if radius == None:
            radius = len(map.map_grid) + len(map.map_grid[0])

        r = 1
        enemy = None
        while not enemy and r < radius:
            potentials = list()
            for i in xrange(x-r,x+r):
                for j in xrange(y-r, y+r):
                    for e in get_entities_on_tile(i,j):
                        if my_team.index(e) == None:
                            potentials.append(e)
            for e in potentials:
                enemy = e if enemy.hp > e.hp else enemy = e
            r += 1
        return enemy

    def find_closest_injured(center, game, radius = None, threshold = 0.5):
        if center is BaseUnit:
            x, y = center.pos
        else:
            x, y = center # Center is a tuple
        
        if radius == None:
            radius = len(map.map_grid) + len(map.map_grid[0])

        patient = BaseUnit()
        patient.hp = maxint
        for u in my_team:
            if u.hp < u.base_stats['health']*threshold:
                distance = sqrt((u.pos[0]-x)**2+(u.pos[1]-y)**2)
                if distance < radius:
                    patient = u if u.hp < patient.hp
        return patient
