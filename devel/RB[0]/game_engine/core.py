

class UnitType(object):
    def __init__(self, type="None",
                 hitpoints=10, magicpoints=10,
                 speed=5,
                 armor = {"None":50}):

        self.type = type

        self.hitpoints = hitpoints
        self.magicpoints = magicpoints

        self.speed = speed

        self.armor = armor

class Unit(object):
    def __init__(self, unit_type, player_num=0,
                 hitpoints=10, magicpoints=10,
                 effects=[], abilities=[],
                 pos=(0,0,0)):

        self.unit_type = unit_type

        self.player_num = player_num

        self.max_hitpoints = self.unit_type.hitpoints
        if hitpoints:
            self.cur_hitpoints = hitpoints
        else:
            self.cur_hitpoints = int(self.unit_type.max_hitpoints)

        self.max_magicpoints = self.unit_type.magicpoints
        if magicpoints:
            self.cur_magicpoints = magicpoints
        else:
            self.cur_magicpoints = int(self.unit_type.max_magicpoints)

        self.max_speed = self.unit_type.speed
        self.cur_speed = int(self.unit_type.speed)

        self.max_armor = self.unit_type.armor
        self.cur_armor = dict(self.unit_type.armor)

        self.effects = effects
        self.abilities = abilities

        self.pos = pos #pos is the x, y, pos plus the "layer" the units is on,
                       #eg 0 is the highest point of the lowest block of terrain at this point

    def update(self):
        for i in self.effects:
            if i.dead:
                self.effects.remove(i)
            i.update(self)

        return None

    def use_ability(self, ability, all_units):
        ability.use_cost(self)
        for i in all_units:
            a = ability.check_apply(self, i)
            if a:
                i.effects.extend(ability.effects)

        return None


def check_square(spos, ran, epos):
    if spos[2] != epos[2]:
        return False
    for x in xrange(pos[0]-ran, pos[0]+ran):
        for y in xrange(pos[1]-ran, pos[1]+ran):
            if epos == (x, y, pos[2]):
                return True
    return False

def check_cross(spos, ran, epos):
    if spos[2] != epos[2]:
        return False
    for x in xrange(pos[0]-ran, pos[0]+ran):
        if epos == (x, pos[1], pos[2]):
            return True
    for y in xrange(pos[1]-ran, pos[1]+ran):
        if epos == (pos[0], y, pos[2]):
            return True
    return False

def check_target(spos, ran, epos):
    if spos[2] != epos[2]:
        return False
    dis = max((abs(spos[0] - epos[0]),
               abs(spos[1] - epos[1])))
    return dis <= ran

class Ability(object):
    def __init__(self, effects=[],
                 cost = {},
                 target="Self",
                 range=0, shape="Target"):

        self.effects = effects
        self.cost = cost

        self.target = target
        self.range = range
        self.shape = shape

    def use_cost(self, unit):
        for i in self.cost:
            a = getattr(unit, i)
            a += self.cost[i]
            setattr(unit, i, a)
        return None

    def check_apply(self, caster, target):
        #this should be run against all other units in the game
        if self.target == "Self":
            if caster == target:
                return True

        if self.shape == "Target":
            shape = check_target(caster.pos, self.range, target.pos)
        elif self.shape == "Square":
            shape = check_square(caster.pos, self.range, target.pos)
        else: #is a cross
            shape = check_cross(caster.pos, self.range, target.pos)

        if not shape:
            return False

        if self.target == "Enemies":
            if target.player_num == caster.player_num:
                return False
            return True
        if self.target == "Allies":
            if target.player_num == caster.player_num:
                return True
            return False
        if self.target == "All":
            return True
        return False

class Effect(object):
    def __init__(self, type="None",
                 affect={},
                 duration=0):

        self.type = type
        self.affect = affect

        self.duration = duration
        self.cur_age = 0

        self.dead = False

    def update(self, unit):

        for i in self.affect:
            a = getattr(unit, i)
            a += self.affect[i]
            setattr(unit, i, a)

        self.cur_age += 1
        if self.cur_age >= self.duration:
            self.dead = True
