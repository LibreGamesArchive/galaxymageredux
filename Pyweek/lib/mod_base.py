import load_mod_file
import glob, os

class Ability(object):
    '''Base Action class'''
    def __init__(self, parent):
        self.unit = parent
        self.cost = 0
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
    def __init__(self, scenario):
        self.scenario = scenario

        # Gfx Attributes
        self.name = ''
        self.pos = (0,0)
        self.level = 1
        self.image = ''
        self.gfx_entity = None
        
        # Battle Attributes
        self.hp = 0
        self.strength = 0
        self.action_points = 0
        self.dead = False
        self.team = ''
        self.base_stats = {}
        self.abilities = self.scenario.abilh.abilities
        self.actions = {}

        self.initialize()

        self.cur_hp = int(self.hp)
        self.cur_ap = int(self.action_points)

    def initialize(self):
        pass

    def load_stats(self, stats):
        self.name, self.pos, self.level = stats


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

class Scenario(object):
    def __init__(self, engine, scenario):
        self.engine = engine

        self.abilh = AbilityHandler()
        self.abilh.load_dir('data/scenarios/%s/abilities/'%scenario)
        self.abilh.load_dir('data/abilities/')

        self.unith = UnitHandler(self)
        self.unith.load_dir('data/scenarios/%s/units/'%scenario)
        self.unith.load_dir('data/units/')

        access = {'Unit':self.make_unit,
                  'engine':self.engine,
                  'parent':self}
        store = load_mod_file.load('data/scenarios/%s/scenario.py'%scenario, access)
        if store == False:
            print 'fail load scenario <%s>'%scenario
        else:
            self.mod = store.scenario

        self.units = []

        self.mod.initialize()

    def make_unit(self, type, team, stats):
        new = self.unith.units[type](self)
        new.load_stats(stats)
        new.team = team
        new.gfx_entity = self.engine.gfx.mapd.make_entity(new.image, new.pos, new.name)
        self.units.append(new)

    def update(self):
        self.mod.update()
