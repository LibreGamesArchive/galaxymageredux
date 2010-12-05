class Color(object):
    def __init__(self, val, form=None):
        a = None
        if isinstance(val, Color):
            r, g, b, a = val.r, val.g, val.b, val.a
            form = 'rgba1'
        elif val == None:
            r,g,b,a = 0,0,0,0
            form = 'rgba1'
        elif len(val) == 3:
            r,g,b = val
        else:
            r,g,b,a = val

        if form == None:
            if max(val) <= 1:
                form = 'rgba1'
            else:
                form = 'rgba255'
            if a == None:
                if form == 'rgba1': a = 1
                else: a = 255

        if form == "rgba255":
            r,g,b,a = map(self.convert_255_to_1, (r,g,b,a))

        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def convert_255_to_1(self, val):
        return val*1.0/255 if val else 0

    def get_rgb1(self):
        return self.r, self.g, self.b

    def get_rgb255(self):
        return map(int, (self.r*255, self.g*255, self.b*255))

    def get_rgba1(self):
        return self.r, self.g, self.b, self.a

    def get_rgba255(self):
        return map(int, (self.r*255, self.g*255, self.b*255, self.a*255))
