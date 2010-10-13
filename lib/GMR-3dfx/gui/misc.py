class RelativePos(object):
    """makes a position relative to the parent"""
    def __init__(self, x="left", y="bottom", to=None, padx=0, pady=0):
        self.x = x
        self.y = y
        self.padx = padx
        self.pady = pady
        self.to = to

    def get_pos(self):
        if self.to:
            rel = self.to
            relx, rely = rel.pos.get_pos()
            if self.x == "left":
                x = relx
            elif self.x == "center":
                x = relx + int(rel.size[0]*0.5)
            else:
                x = relx + rel.size[0]

            if self.y == "top":
                y = rely
            elif self.y == "center":
                y = rely + int(rel.size[1]*0.5)
            else:
                y = rely + rel.size[1]

            return x+self.padx, y+self.pady

        return self.padx, self.pady

    def get_real_pos(self):
        if self.to:
            rel = self.to
            px, py = rel.get_real_pos()
            if self.x == "left":
                x = px
            elif self.x == "center":
                x = px + int(rel.size[0]*0.5)
            else:
                x = px + rel.size[0]

            if self.y == "top":
                y = py
            elif self.x == "center":
                y = py + int(rel.size[1]*0.5)
            else:
                y = py + rel.size[1]

            return x+self.padx, y+self.pady
        else:
            return self.padx, self.pady

class AbsolutePos(object):
    def __init__(self, pos):
        self.x, self.y = pos

    def get_pos(self):
        return self.x, self.y
