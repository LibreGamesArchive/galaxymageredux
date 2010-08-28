import load_mod_file, gui
import glob, os
from math import sqrt, sin, cos, pi

class Ability(object):
    '''Base Action class'''
    def __init__(self, parent):
        self.unit = parent
        self.cost = 0
        self.desc = 'Action <costs 0 AP>'
        self.name = 'Action'
        self.initialize()

    def initialize(self):
        pass

    def test_available(self):
        return True

    def test_acceptable(self, target):
        return True

    def perform(self, target):
        return False

    def render_select(self):
        pass

    def get_select(self):
        pass

class AbilityHandler(object):
    def __init__(self):
        self.abilities = {}

    def load_dir(self, path):
        self.abilities = {}
        access = {'BaseAbility':Ability}
        for ability in glob.glob(path+'*.py'):
            name = os.path.split(ability)[1].split('.')[0]
            store = load_mod_file.load(ability, access)
            if store == False:
                print 'fail load ability <%s>'%ability
            else:
                self.abilities[name] = store.ability

class Unit(object):
    type = 'base'
    last_gid = 0
    def __init__(self, scenario):
        self.scenario = scenario

        # Gfx Attributes
        self.name = ''
        self.pos = (0,0)
        self.level = 1
        self.image = ''
        self.gfx_entity = None
        self.team_flag = None
        self.desc = 'BaseUnit desciption'
        self.boost_hp = 1
        self.boost_strength = 1
        self.dead = False
        
        # Battle Attributes
        self.hp = 0
        self.strength = 0
        self.action_points = 0

        self.team = ''
        self.base_stats = {}
        self.abilities = self.scenario.abilh.abilities
        self.actions = []

        self.initialize()

        self.cur_hp = int(self.hp)
        self.cur_ap = int(self.action_points)
        self.gid = self.last_gid
        self.strength += self.boost_strength*(self.level-1)
        self.hp += self.boost_hp*(self.level-1)
        self.cur_hp = int(self.hp)
        Unit.last_gid += 1

    def initialize(self):
        pass

    def have_ability(self, name):
        self.actions.append(self.abilities[name](self))

    def load_stats(self, stats):
        self.name, self.pos, self.level = stats

    def update(self):
        if self.hp <= 0:
            self.hp = 0
            self.dead = True
            self.gfx_entity.kill()
            self.team_flag.kill()

        self.gfx_entity.pos = self.pos
##        self.team_flag.pos = self.pos[0], self.pos[1]+0.01


class UnitHandler(object):
    def __init__(self, scenario):
        self.scenario = scenario
        self.units = {}

    def load_dir(self, path):
        self.units = {}
        access = {'BaseUnit':Unit}
        for unit in glob.glob(path+'*.py'):
            store = load_mod_file.load(unit, access)
            if store == False:
                print 'fail load unit <%s>'%unit
            else:
                self.units[store.unit.type] = store.unit

class AI(object):
    def __init__(self, scenario, team):
        self.scenario = scenario
        self.team = team

        self.initialize()

    def initialize(self):
        pass

    def end_my_turn(self):
        self.scenario.engine.endMyTurn()
        self.scenario.engine.engine.sendMessage('<AI> I end turn')
    
    def do_action(self, unit, action, target):
        action.perform(target)
    
    def get_my_units(self):
        bucket = []
        for u in self.scenario.units:
            if u.team == self.team:
                bucket.append(u)
        return bucket

    def get_enemy_units(self):
        bucket = []
        for u in self.scenario.units:
            if u.team != self.team:
                bucket.append(u)
        return bucket

    # Path search utility functions
    def distance(self, a, b):
        return abs(a[0]-b[0]) + abs(a[1]-b[1])

    def get_neighbors(self, x):
        for i in range(0,3):
            yield (int(cos(i*0.5*pi)+x[0]),
                   int(sin(i*0.5*pi)+x[1]))

    def get_next_tile(self, start, goal):
        '''TODO: update to a proper a_star search '''
        s = start.pos
        g = goal.pos
        next = s
        for n in self.get_neighbors(s):
            if n == goal:
                return s
            if next == s:
                next = n
            if self.distance(next,g) > self.distance(n,g):
                next = n
        return next
    
    def tile_weight(self, v):
        return 0 # TODO: implement any hinderence that map can cause.

    def estimate(self, a, b):
        '''This needs to be tweaked. It really only works for a rectangular
        plane with no gaps, barriers or other hinderences'''
        return self.distance(a,b)

    def reconstruct(self, node, dgraph):
        if repr(node) in directed_graph.keys():
            return reconstruct(dgraph[repr(node)],dgraph) + [node]
        else:
            return [node]

    def valid_tile(self, v):
        map = self.scenario.engine.mapd

        # Test out bounds
        if 0 > v[1] or v[1] < len(map) or 0 > v[0] or v[0] > len(map[v[1]]):
            return False

        # Test for blocking unit (Assuming that all units will block)
        for u in self.scenario.units:
            if int(u.pos[0]) == v[0] or int(u.pos[1]) == v[1]:
                return False 

        # Test for blocking MapEntity(somewhat redundant?)
        # Assumes all MapEntities block
        for u in self.scenario.engine.gfx.mapd:
            if int(u.pos[0]) == v[0] or int(u.pos[1]) == v[1]:
                return False

    def get_path(self, start, goal):
        ''' Start and Goal are (row,column) tuples. Returns best path from
        start to goal, inclusive, as a list of (row,column) tuples. If a path cannot be
        found, returns None'''
        start = (int(start[0]), int(start[1]))
        goal = (int(goal[0]), int(goal[1]))

        open = set([start])
        closed = set()

        G = {repr(start):0}
        H = {repr(start):estimate(start,goal)}
        F = {repr(start):H[repr(start)]}

        directed_graph = {}
        while len(open):
            cur = list(open)[0]
            for v in open:
                if F[repr(v)] < F[repr(cur)]: cur = v

            if cur in open:
                open.remove(cur)
                closed.add(cur)
            else:
                print("Error in AI.get_path. <hatemail: durandal@gmail.com>")
                return None # Hopefully not, though

            for v in self.get_neighbors(cur):
                if v == goal:
                    return reconstruct(cur, directed_graph) + [goal]

                if v in closed or not self.valid_tile(v):
                    continue

                if v in open:
                    pass
                else:
                    directed_graph[repr(v)] = cur
                    open.add(v)
                    G[repr(v)] = 0
                    H[repr(v)] = self.estimate(v,goal)
                    F[repr(v)] = G[repr(v)] + H[repr(v)] + self.tile_weight(v)

        return None #Really?

class BaseScenario(object):
    def __init__(self):
        self.initialize()

    def game_over(self):
        return False

class Scenario(object):
    def __init__(self, engine, scenario):
        self.engine = engine

        self.abilh = AbilityHandler()
        self.abilh.load_dir('data/scenarios/%s/abilities/'%scenario)
        self.abilh.load_dir('data/abilities/')

        self.unith = UnitHandler(self)
        self.unith.load_dir('data/scenarios/%s/units/'%scenario)
        self.unith.load_dir('data/units/')

        self.units = []

        store = load_mod_file.load('data/scenarios/%s/config.py'%scenario)
        if store == False:
            print 'fail load config <%s>'%scenario
        else: self.config = store

        access = {'Unit':self.make_unit,
                  'engine':self.engine,
                  'parent':self,
                  'BaseScenario':BaseScenario,
                  'gui':gui}
        store = load_mod_file.load('data/scenarios/%s/scenario.py'%scenario, access)
        if store == False:
            print 'fail load scenario <%s>'%scenario
        else:
            self.mod = store.scenario()

        access = {'BaseAI':AI}
        store = load_mod_file.load('data/scenarios/%s/ai.py'%scenario, access)
        if store == False:
            print 'fail load ai <%s>'%scenario
        else:
            self.core_ai = store.ai

        self.ai_players = []

    def make_ai_player(self, team):
        new = self.core_ai(self, team)
        self.ai_players.append(new)

    def make_unit(self, type, team, stats):
        new = self.unith.units[type](self)
        new.load_stats(stats)
        new.team = team
        new.gfx_entity = self.engine.gfx.mapd.make_entity(new.image, new.pos, new.name, 'center')
        new.team_flag = self.engine.gfx.mapd.make_entity('player-team-flag.png'+str(self.config.teams.index(team)),
                                                       new.pos, new.name+'_flag', 'center')
        new.team_flag.bound_to = new.gfx_entity
        new.update()
        self.units.append(new)

    def update(self):
        if self.engine.engine.am_master:
            turn = self.engine.engine.whos_turn
            for i in self.ai_players:
                if i.team == turn:
                    i.update()
        try:
            self.mod.update()
        except:
            pass

    def winner(self):
        return self.mod.game_over()
