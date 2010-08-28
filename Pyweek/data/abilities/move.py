

class Ability(BaseAbility):
    def initialize(self):
        self.cost = 1
        self.desc = 'Move <cost 1 AP>'

    def test_available(self):
        mapd = self.unit.scenario.engine.gfx.mapd #yikes!
        if self.unit.cur_ap >= 2: #can't be last action!
            return True

    def get_select(self):
        ap = self.unit.cur_ap
        cx, cy = self.unit.pos
        cx = int(cx)
        cy = int(cy)

        pos = []

        for y in xrange(ap):
            for x in xrange(ap-y):
                if (x,y) == (0,0):
                    continue

                if x+y <= ap:
                    pos.extend([
                        (cx+x,cy+y),
                        (cx-x,cy+y),
                        (cx-x,cy-y),
                        (cx+x,cy-y)])

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

store.ability = Ability
