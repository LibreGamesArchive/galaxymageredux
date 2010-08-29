
class Ability(BaseAbility):
    def initialize(self):
        self.cost = 1
        self.desc = 'Move <cost 1 AP>'
        self.name = 'Move'

    def test_available(self):
        if self.unit.cur_ap >= 2: #can't be last action!
            return True

    def test_acceptable(self, target):
        return target in self.get_select()

    def _get_blocked_tiles(self):
        tiles = []
        for i in self.unit.scenario.units:
            if i.team != self.unit.team and i.dead == False:
                tiles.append(i.pos)

        for i in self.unit.scenario.engine.gfx.mapd.entities:
            if i.name == 'blocking':
                tiles.append(i.pos)

        passable = []
        for i in self.unit.scenario.units:
            if i.team == self.unit.team and i.dead == False:
                if not i in tiles:
                    passable.append(i.pos)

        return tiles, passable

    def get_select(self):
        ap = self.unit.cur_ap-1
        cx, cy = self.unit.pos
        cx = int(cx)
        cy = int(cy)

        pos = []

        blocked, passable = self._get_blocked_tiles()
        mapd = self.unit.scenario.engine.gfx.mapd #yikes!

        for y in xrange(ap*2+1):
            y -= ap
            for x in xrange(ap*2+1-y):
                x -= ap
                if (x,y) == (0, 0):
                    continue

                if abs(x) + abs(y) <= ap:
                    n = cx+x, cy+y
                    if mapd.in_bounds(n) and (not n in blocked+passable):
                        p = self.get_path((cx,cy), n, blocked)
                        if p and len(p[1:]) <= ap:
                            pos.append((cx+x,cy+y))

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
        xx, xy = self.unit.pos
        self.unit.pos = target
        price = abs(target[0]-xx)+abs(target[1]-xy)
        self.unit.cur_ap -= price

        self.unit.update()


    #A* stuff!
    def distance(self, a, b):
        return abs(a[0]-b[0]) + abs(a[1]-b[1])

    def get_neighbors(self, x):
        yield x[0]-1, x[1]
        yield x[0]+1, x[1]
        yield x[0], x[1]-1
        yield x[0], x[1]+1

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
        if repr(node) in dgraph.keys():
            return self.reconstruct(dgraph[repr(node)],dgraph) + [node]
        else:
            return [node]

    def valid_tile(self, v, blocked):
        mapd = self.unit.scenario.engine.gfx.mapd #yikes!
        # Test out bounds
        if not mapd.in_bounds(v):
            return False

        return v not in blocked

    def get_path(self, start, goal, blocked):
        ''' Start and Goal are (row,column) tuples. Returns best path from
        start to goal, inclusive, as a list of (row,column) tuples. If a path cannot be
        found, returns None'''
        start = (int(start[0]), int(start[1]))
        goal = (int(goal[0]), int(goal[1]))

        open = set([start])
        closed = set()

        G = {repr(start):0}
        H = {repr(start):self.estimate(start,goal)}
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
                print("Error in AI.get_path.")
                return None # Hopefully not, though

            for v in self.get_neighbors(cur):
                if v == goal:
                    return self.reconstruct(cur, directed_graph) + [goal]

                if v in closed or not self.valid_tile(v, blocked):
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

store.ability = Ability
