
import math

def safe_div(x, y):
    if x and y:
        return x / y
    return 0

class Vector(object):
    otype = "Vector"
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

        self.backups = []

    def __backup(self):
        self.backups.append((self.x, self.y, self.z))
    backup = __backup

    def __restore(self):
        a = self.backups.pop(-1)
        if a:
            self.x, self.y, self.z = a
    restore = __restore

    def __make_new(self, vector, func):
        self.__backup()
        func(vector)
        new = self.x, self.y, self.z
        self.__restore()
        return Vector(*new)

    def add(self, vector):
        self.x += vector.x
        self.y += vector.y
        self.z += vector.z
        return self

    def __add__(self, other):
        return self.__make_new(other, self.add)
    def nadd(self, other):
        return self.__make_new(other, self.add)

    def inc(self, vector):
        if self.x >= 0:
            self.x += vector.y
        else:
            self.x -= vector.y
        if self.y >= 0:
            self.y += vector.y
        else:
            self.y -= vector.y
        if self.z >= 0:
            self.z += vector.z
        else:
            self.z -= vector.z
        return self

    def ninc(self, other):
        return self.__make_new(other, self.inc)

    def sub(self, vector):
        self.x -= vector.x
        self.y -= vector.y
        self.z -= vector.z
        return self

    def __sub__(self, other):
        return self.__make_new(other, self.sub)
    def nsub(self, other):
        return self.__make_new(other, self.sub)

    def dec(self, vector):
        if self.x >= 0:
            self.x -= vector.x
            if self.x < 0:
                self.x = 0
        else:
            self.x += vector.x
            if self.x > 0:
                self.x = 0
        if self.y >= 0:
            self.y -= vector.y
            if self.y < 0:
                self.y = 0
        else:
            self.y += vector.y
            if self.y > 0:
                self.y = 0
        if self.z >= 0:
            self.z -= vector.z
            if self.z < 0:
                self.z = 0
        else:
            self.z += vector.z
            if self.z > 0:
                self.z = 0
        return self

    def ndec(self, other):
        return self.__make_new(other, self.dec)

    def mult(self, vector):
        self.x *= vector.x
        self.y *= vector.y
        self.z *= vector.z
        return self

    def __mul__(self, other):
        return self.__make_new(other, self.mult)
    def nmult(self, other):
        return self.__make_new(other, self.mult)

    def div(self, vector):
        self.x = safe_div(self.x, vector.x)
        self.y = safe_div(self.y, vector.y)
        self.z = safe_div(self.z, vector.z)
        return self

    def __div__(self, other):
        return self.__make_new(other, self.div)
    def ndiv(self, other):
        return self.__make_new(other, self.div)

    def invert(self):
        self.x = -self.x
        self.y = -self.y
        self.z = -self.z
        return self

    def rotate(self, x, y, z, pos=(0,0,0)):
        sx, sy, sz = self.x, self.y, self.z
        sx -= pos[0]
        sy -= pos[1]
        sz -= pos[2]
        if x:
            radians = math.radians(-x)
            cos = math.cos(radians)
            sin = math.sin(radians)
            ox, oy, oz = float(sx), float(sy), float(sz)

            sy = (cos * oy) - (sin * oz)
            sz = (sin * oy) + (cos * oz)

        if y:
            radians = math.radians(-y)
            cos = math.cos(radians)
            sin = math.sin(radians)
            ox, oy, oz = float(sx), float(sy), float(sz)

            sx = (cos * ox) - (sin * oz)
            sz = (sin * ox) + (cos * oz)

        if z:
            radians = math.radians(-z)
            cos = math.cos(radians)
            sin = math.sin(radians)
            ox, oy, oz = float(sx), float(sy), float(sz)

            sx = (cos * ox) - (sin * oy)
            sy = (sin * ox) + (cos * oy)

        sx += pos[0]
        sy += pos[1]
        sz += pos[2]
        self.x, self.y, self.z = sx, sy, sz
        return self

    def get_distance(self, vector):
        new = Vector(self.x, self.y, self.z)
        new.sub(vector)
        return new.length()

    def length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def scale(self, constant):
        assert constant != 0
        self.multiply(Vector(constant, constant, constant))
        return self

    def unit(self):
        len = self.length()
        return Vector(safe_div(self.x, len),
                      safe_div(self.y, len),
                      safe_div(self.z, len))

    def dot(self, vector):
        return self.x * vector.x + self.y * vector.y + self.z * vector.z

    def cross(self, vector):
        x = self.y * vector.y - self.z * vector.z
        y = self.z * vector.x - self.x * vector.z
        z = self.x * vector.y - self.y * vector.x
        return Vector(x, y, z)

    def pos(self):
        return self.x, self.y, self.z

    def normalize(self):
        self.x = safe_div(self.x, self.length())
        self.y = safe_div(self.y, self.length())
        self.z = safe_div(self.z, self.length())
        return self

    def normalized(self):
        return Vector(safe_div(self.x, self.length()),
                      safe_div(self.y, self.length()),
                      safe_div(self.z, self.length()))
