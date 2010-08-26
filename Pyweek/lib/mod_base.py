import load_mod_file
import glob

class Unit(object):
    type = 'base'
    def __init__(self):
        self.name = ''
        self.pos = (0,0)
        self.level = 1
        self.image = ''

        self.stats = {}


class UnitHolder(object):
    def __init__(self):
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
