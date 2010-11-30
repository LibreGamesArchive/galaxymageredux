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
            pad = rel.get_padding()
            relx, rely = rel.get_pos()
            rsize = rel.get_size()
            if self.x == "left":
                x = relx
            elif self.x == "center":
                x = relx + int(rsize[0]*0.5) + pad[0]
            else:
                x = relx + rsize[0] + pad[0] + pad[1]

            if self.y == "top":
                y = rely
            elif self.y == "center":
                y = rely + int(rsize[1]*0.5) + pad[2]
            else:
                y = rely + rsize[1] + pad[2] + pad[3]

            return x+self.padx, y+self.pady

        return self.padx, self.pady

    def get_real_pos(self):
        if self.to:
            rel = self.to
            pad = rel.get_padding()
            px, py = rel.get_real_pos()
            rsize = rel.get_size()
            if self.x == "left":
                x = px
            elif self.x == "center":
                x = px + int(rsize[0]*0.5) + pad[0]
            else:
                x = px + rsize[0] + pad[0] + pad[1]

            if self.y == "top":
                y = py
            elif self.x == "center":
                y = py + int(rsize[1]*0.5) + pad[2]
            else:
                y = py + rsize[1] + pad[2] + pad[3]

            return x+self.padx, y+self.pady
        else:
            return self.padx, self.pady

class AbsolutePos(object):
    def __init__(self, pos):
        self.x, self.y = pos

    def get_pos(self):
        return self.x, self.y
