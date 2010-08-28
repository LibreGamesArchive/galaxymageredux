
class Ability(BaseAbility):
    def initialize(self):
        self.cost = 2
        self.desc = 'Bow Attack <range: 2, cost 2 AP>'
        self.name = 'Bow Attack'

        self.range = 2

    def test_available(self):
        if self.unit.cur_ap >= 2: #can't be last action!
            if self.get_select():
                return True

    def test_acceptable(self, target):
        return target in self.get_select()

    def get_select(self):
        cx, cy = self.unit.pos
        cx = int(cx)
        cy = int(cy)

        mapd = self.unit.scenario.engine.gfx.mapd #yikes!

        pos = []

        units = self.unit.scenario.units

        for y in xrange(self.range*2+1):
            y -= self.range
            for x in xrange(self.range*2+1):
                x -= self.range
                if (x,y) == (0, 0):
                    continue

                n = cx+x, cy+y
                if mapd.in_bounds(n):
                    for i in units:
                        if i.pos == n and i.team != self.unit.team:
                            pos.append(n)

        return pos

    def render_select(self):
        #TODO: add dodging of obstacles!
        mapd = self.unit.scenario.engine.gfx.mapd #yikes!
        ap = self.unit.cur_ap
        cx, cy = self.unit.pos
        cx = int(cx)
        cy = int(cy)

        pos = self.get_select()

        mapd.clear_highlights()
        for i in set(pos):
            if mapd.in_bounds(i):
                mapd.add_highlight('gui_mouse-hover2.png', i)

    def perform(self, target):
        units = self.unit.scenario.units
        for i in units:
            if i.pos == target and i.team != self.unit.team:
                i.cur_hp -= int(self.unit.strength*0.5)
                self.unit.cur_ap -= self.cost
                i.update()
                self.unit.update()

store.ability = Ability
