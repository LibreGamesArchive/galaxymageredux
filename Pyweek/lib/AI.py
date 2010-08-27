""" Artificial Intelligence
    Really just a static class with some public decision-making methods.
    1. Could be overloaded in the future to give decisions attributes like:
       aggression or survivalism.
    Robert Ramsay
"""
from mod_base import Unit
from math import sqrt, pi, cos, sin, tan
from sys import maxint

class AI_Player:
    def __init__(self, my_team, engine):
        self.team = my_team
        self.engine = engine

    def update(self):
        ''' Calling this assumes it is the AI's turn. Fairly dumb and agressive
        AI. Always rushes, always attacks.'''
        for unit in self.team:
            # TODO: give each unit a target preference/priority list: closest, weakest, type
            closest_enemy = find_closest_enemy(unit, self.engine.mapd)
            path = a_star(unit,closest_enemy,self.engine.mapd)# find path using a_star
            if path:
                move_along_path(unit, path)
            unit.attack(closest_enemy)

    def ValidSquare(self, x, y, map):
        ''' This will be replaced with a real check later, either here or by
        a method in MapHandler.
        Check for:
            Blocking Entities/Walls
            Point off map
            Distance not jumpable by unit
        '''
        return True

# A* Search utility functions

    def neighbor_nodes(self, x):
        '''Neighbor node generator'''
        i = 0.0
        while i < 2*pi:
            yield (int(cos(i))+x[0], int(sin(i))+x[1])
            i += pi*0.5

    def distance(self, a, b):
        ''' The Distance between two (x,y) tuples '''
        return int(sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)+0.5)

    def _reconstruct(self, node):
        if came_from[repr(node)] is type(set):
            p[reconstruct_path(came_from[repr(node)])]
            return p.append(node)
        else:
            return node

# End A* utility functions

    def tile_weight(self, node):
        '''Gets weight of tiles, from map or something'''
        if len(self.engine.map) < node[1] or len(self.engine.map[len(self.engine.map)/2]):
            return maxint
        if self.engine.map(node) == (Wall or Water or Hole or Offmap):
            return maxint
        for e in self.engine.entities:
            if self.team.index(e):
                return 0
            else:
                return maxint

    def heuristic_estimate_of_distance(self, start, goal, map):
        '''Guess based on "barrier" density and area between start and goal'''
        return 2 * abs((start[0]-goal[0])*(start[1]-goal[1]))+len(map.entities)/(len(map)*len(map[len(map)/2]))
    def a_star(self, center, target, map):
        
        start = center.pos() if center is Unit else center
        goal = target.pos() if target is Unit else target
        
        closedset = set()    
        openset = set([start])
        g_score = {repr(start):0}      # Distance from start along optimal path.
        h_score = {repr(start):heuristic_estimate_of_distance(start, goal)}
        f_score = {repr(start):h_score[repr(start)]} # Estimated total distance from start to goal through y.
        x = start
        while openset:
            for n in openset: #find node in openset having the lowest f_score
                if f_score[repr(n)] < f_score[repr(x)]: x = n 
            
            if x == goal:
                return reconstruct_path(came_from[repr(goal)])
            
            openset.remove(x)
            closedset.add(x)
            
            for y in neighbor_nodes(x):
                if y in closedset:
                    continue
                tentative_g_score = g_score[repr(x)] + distance(x,y) + tile_weight(x)
                
                if y not in openset:
                    openset.add(y) 
                    tentative_is_better = True
                elif tentative_g_score < g_score[repr(y)]:
                    tentative_is_better = True
                else:
                    tentative_is_better = False
                if tentative_is_better == True:
                    came_from[repr(y)] = x
                    g_score[repr(y)] = tentative_g_score
                    h_score[repr(y)] = heuristic_estimate_of_distance(y, goal)
                    f_score[repr(y)] = g_score[repr(y)] + h_score[repr(y)]
        return None #Really?

    def find_closest_enemy(self, center, map, radius = None):
        '''Searches until it finds an enemy. radius limits how far from the
        center we can look.'''
        if radius == None:
            radius = len(map.map_grid) + len(map.map_grid[0])

        enemy = None
        for e in self.engine.entities:
            if e not in self.team:
                d = distance(e,center)
                if d < radius and d < distance(enemy,center):
                    enemy = e
        return enemy

    def find_closest_injured(self, center, game, radius = None, threshold = 0.5):
        if center is Unit:
            x, y = center.pos
        else:
            x, y = center # Center is a tuple
        
        if radius == None:
            radius = len(map.map_grid) + len(map.map_grid[0])

        patient = Unit()
        patient.hp = maxint
        for u in my_team:
            if u.hp < patient.hp and u.hp < u.base_stats['health']*threshold and distance(u,(x,y)):
                patient = u
        return patient

if __name__ == '__main__':
    print('Initializing base AI_Player')
    ai = AI_Player()
    # Test Neighbor generator
    print('Testing neighbor_nodes')
    for n in ai.neighbor_nodes((0,0)):
        print(n)
    