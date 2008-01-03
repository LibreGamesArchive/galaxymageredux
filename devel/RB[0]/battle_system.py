from copy import copy

def safe_div(x, y):
    if x and y:
        return x/y
    return 0

class Attribute(object):
    def __init__(self, max_value, start_value=None):
        self.max_value = max_value
        if start_value:
            self.value = start_value
        else:
            self.value = copy(self.max_value) #done so that you don't modify max_value

class ArmorType(object):
    def __init__(self, values={"type":"amount"}):
        self.values = values

class Ability(object):
    def __init__(self, target="All", effects=[],
                 range=5, shape="Cone",
                 splash_range=1):
        self.target = target

        self.effects = effects

        self.range = range
        self.shape = shape
        self.splash_range = splash_range

##    def get_hs_line(self, start, end):
##        dx = end[0] - start[0]
##        dy = end[1] - start[1]
##        m = safe_div(float(dx), dy)
##        y = start[1]
##        x = start[0]
##
##        points = []
##        while x <= end[0]:
##            points.append((x, int(y)))
##            x += m
##            y += 1
##        return points
##
##    def get_hs_rect(self, start, end):
##        points = []
##        for x in xrange(start[0] - self.range, start[0] + self.range):
##            for y in xrange(start[1] - self.range, start[1] + self.range):
##                points.append((x, y))
##        return points
##
##    def get_hs_cross(self, start, end):
##        points = []
##        for x in xrange(-self.range, self.range):
##            for y in xrange(-self.range, self.range):
##                if abs(x) + abs(y) < self.range:
##                    points.append((x, y))
##
##    def get_hit_spaces(self, start, end):
##        #end is only used sometimes, like when it is a line or a cone
##        if self.shape == "Line":
##            return self.get_hs_line(start, end)
##        if self.shape == "Rect":
##            return self.get_hs_rect(start, end)
##        if self.shape == "Cross":
##            return self.get_hs_cross(start, end)

class Effect(object):
    def __init__(self, duration=1,
                 modify=[]):

        self.duration = duration
        self.modify = modify

        self.age = 0

    def execute(self, unit):
        for i in self.modify:
            i.execute(unit)

class ModAddAmount(object):
    def __init__(self, attribute="hitpoints", amount=0):
        self.attribute = atttribute
        self.amount = amount

    def execute(self, unit):
        setattr(unit, self.attribute, getattr(unit, self.attribute) + self.amount)

class ModAddArmor(object):
    def __init__(self, type="None"):
        self.type = type

    def execute(self, unit):
        unit.armor.append(self.type)

class ModAddAbility(object):
    def __init__(self, ability=None):
        self.ability = ability

    def execute(self, unit):
        unit.abilities.append(self.ability)


class Unit(object):
    def __init__(self, name="None", gender="Male",
                 hitpoints=25, magicpoints=25
                 speed=5, armor=[],
                 abilites=[],
                 effects = []):

        self.name = name

        self.gender = gender

        self.hitpoints = Attribute(hitpoints)
        self.magicpoints = Attribute(magicpoints)

        self.speed = Attribute(speed)

        self.armor = armor
        self.abilities = abilities

        self.effects = effects

    def get_abilities(self
