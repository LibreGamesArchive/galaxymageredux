class Color(object):
    def __init__(self, val, form="rgba1"):
        if isinstance(val, Color):
            r, g, b, a = val.r, val.g, val.b, val.a
        elif val == None:
            r,g,b,a = 0,0,0,0
        elif len(val) == 3:
            r,g,b = val
            if form == "rgba1":
                a = 1
            elif form == "rgba255":
                a = 255
            else:
                raise Exception("form must be 'rgba1' or 'rgba255'")
        else:
            r,g,b,a = val

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
