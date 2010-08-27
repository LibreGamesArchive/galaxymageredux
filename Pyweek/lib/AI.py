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
    def update(self, engine):
        ''' Calling this assumes it is the AI's turn'''
        for unit in my_team:
            closest_enemy = find_closest_enemy(unit, eng.mapd)
            move_along_path(unit, closest_enemy, eng.mapd)
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

    def move_along_path(self, center, target, map, radius):
        ''' Makes best attempt to find a legal path to location and then move
        unit.'''
        if center is Unit:
            x, y = center.pos
        else:
            x, y = center # Center is a tuple
        x = float(x)
        y = float(y)
        
        if target is Unit:
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
        if center is Unit:
            center.move(x,y)
        return x, y

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
                tentative_g_score = g_score[repr(x)] + distance(x,y)
                
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
        '''Searches until it finds an enemy. center may be the Unit searching
        for an enemy or a (col, row) tuple. radius limits how far from the
        center we can look.'''
        if center is Unit:
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
                if enemy.hp > e.hp: enemy = e # May not be fair, depends on what human players can know.
            r += 1
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
    