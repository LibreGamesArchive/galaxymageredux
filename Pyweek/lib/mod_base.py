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
        if self.cur_hp <= 0:
            self.cur_hp = 0
            self.dead = True
            self.gfx_entity.kill()

        self.gfx_entity.pos = self.pos


class UnitHandler(object):
    def __init__(self, scenario):
        self.scenario = scenario
        self.units = {}

    def load_dir(self, path):
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
            if u.team == self.team and u.dead == False:
                bucket.append(u)
        return bucket

    def get_enemy_units(self):
        bucket = []
        for u in self.scenario.units:
            if u.team != self.team and u.dead == False:
                bucket.append(u)
        return bucket

    # Path search utility functions
    def distance(self, a, b):
        return abs(a[0]-b[0]) + abs(a[1]-b[1])

    def get_neighbors(self, x):
        for i in range(0,3):
            yield (int(cos(i*0.5*pi)+x[0]),
                   int(sin(i*0.5*pi)+x[1]))

class BaseScenario(object):
    def __init__(self, engine):
        self.engine = engine
        self.initialize()

    def winner(self):
        return False

    def closeScenarioMess(self):
        pass

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
            self.mod = store.scenario(self)

        access = {'BaseAI':AI}
        store = load_mod_file.load('data/scenarios/%s/ai.py'%scenario, access)
        if store == False:
            print 'fail load ai <%s>'%scenario
        else:
            self.core_ai = store.ai

        self.ai_players = []

    def setScenarioMess(self, *args, **kwargs):
        self.engine.setScenarioMess(*args, **kwargs)

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
        return new

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
        return self.mod.winner()

    def closeScenarioMess(self):
        self.mod.closeScenarioMess()
