import os
import math

import pygame
from pygame.locals import *

import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *

VERSION = "0.1rc1"

def safe_div(x, y):
    if x and y:
        return x / y
    return 0

def load_texture(file_name):
    tex = glGenTextures(1)
    image = pygame.image.load(file_name)

    x, y = image.get_size()
    nx, ny = 16, 16
    while nx < x:
        nx *= 2
    while ny < y:
        ny *= 2

    image = pygame.transform.scale(image, (nx, ny))
    data = pygame.image.tostring(image, "RGBA", 1)

    glBindTexture(GL_TEXTURE_2D, tex)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.get_width(), image.get_height(),
                 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
    return tex

def load_animation_file(file_name):
    data = open(file_name).read()
    path = os.path.split(file_name)

    animations = {}
    cur_ani = ""

    for line in data:
        if line.startswith("#"):
            continue

        values = line.split()
        if not values:
            continue

        if values[0] == "ver":
            version = values[1]
            if not version == VERSION:
                class BadVersionError(Exception):
                    def __init__(self, value):
                        self.value = value
                    def __str__(self):
                        return repr(self.value)
                raise BadVersionError("requires version %s, got %s"%(VERSION, version))

        if values[0] == "ani":
            animations[values[1]] = []
            cur_ani = values[1]

        if values[0] == "ar":
            animations[cur_ani].append(["ROTATE",
                                        values[1],
                                        map(int, values[2:4]),
                                        map(float, values[4:7])])

        if values[0] == "at":
            animations[cur_ani].append(["TRANSLATE",
                                        values[1],
                                        map(int, values[2:4]),
                                        map(float, values[4:7])])

        if values[0] == "lani":
            animations.update(load_animation_file(os.path.join(path, values[1])))

    return animations

def parse_file(file_name):
    data = open(file_name, "r")
    path = os.path.split(file_name)[0]

    version = ""

    verts = []
    norms = []
    faces = []
    texcs = []

    bones = {}
    bone_connections = []
    animations = {}
    cur_ani = ""

    mtls = {}
    material = None

    objects = {}
    cur_obj = ""

    for line in data:
        if line.startswith("#"):
            continue

        values = line.split()
        if not values:
            continue

        if values[0] == "ver":
            version = values[1]
            if not version == VERSION:
                class BadVersionError(Exception):
                    def __init__(self, value):
                        self.value = value
                    def __str__(self):
                        return repr(self.value)
                raise BadVersionError("requires version %s, got %s"%(VERSION, version))

        if values[0] == "o":
            objects[values[1]] = []
            cur_object = values[1]

        if values[0] == "v":
            verts.append(map(float, values[1:4]))

        if values[0] == "n":
            norms.append(map(float, values[1:4]))

        if values[0] == "tc":
            texcs.append(map(float, values[1:3]))

        if values[0] == "f":
            f = []
            tc = []
            n = []
            for v in values[1:]:
                w = v.split('/')
                f.append(int(w[0]))
                if len(w) >= 2 and len(w[1]) > 0:
                    n.append(int(w[1]))
                else:
                    n.append(0)
                if len(w) >= 3 and len(w[2]) > 0:
                    tc.append(int(w[2]))
                else:
                    tc.append(0)
            f = (f, n, tc, material)
            faces.append(f)
            objects[cur_object].append(f)

        if values[0] == "mtl":
            mtls[values[1]] = {"color":(1, 1, 1, 1),
                               "tex":None}

        if values[0] == "mc":
            mtls[values[1]]["color"] = map(float, values[2:5])

        if values[0] == "mt":
            mtls[values[1]]["tex"] = load_texture(os.path.join(path, values[2]))

        if values[0] == "usemtl":
            material = values[1]

        if values[0] == "b":
            bones[values[1]] = (map(float, values[2:5]),
                                map(float, values[5:8]))

        if values[0] == "cb":
            bone_connections.append([values[1], values[2], int(values[3]), int(values[4])])

        if values[0] == "ani":
            animations[values[1]] = []
            cur_ani = values[1]

        if values[0] == "ar":
            animations[cur_ani].append(["ROTATE",
                                        values[1],
                                        map(int, values[2:4]),
                                        map(float, values[4:7])])

        if values[0] == "at":
            animations[cur_ani].append(["TRANSLATE",
                                        values[1],
                                        map(int, values[2:4]),
                                        map(float, values[4:7])])

        if values[0] == "lani":
            animations.update(load_animation_file(os.path.join(path, values[1])))

    return objects, faces, verts, norms, mtls, texcs, bones, bone_connections, animations

def average_verts(x):
    new = [0,0,0]
    tot = 0
    for i in x:
        new[0] += i[0]
        new[1] += i[1]
        new[2] += i[2]
        tot += 1
    new = [safe_div(new[0], tot),
           safe_div(new[1], tot),
           safe_div(new[2], tot)]
    return new

class Animation(object):
    def __init__(self, name="", data=[]):
        self.name = name
        self.data = data

        self.frames = self.build_data()

    def __get_amount(self, frames, amount):
        return [(float(i) / (frames[1] - frames[0])) for i in amount]

    def build_data(self):
        i = self.data
        new = {}

        mx = max([x[2][1] for x in i])

        for x in i:
            type, name, frames, amount = x

            if not name in new:
                new[name] = [["None"]] * mx

            for i in range(frames[0], frames[1], 1):
                if new[name][i][0] == "None":
                    new[name][i] = [type] + self.__get_amount(frames, amount)
                else:
                    new[name][i][0] += "~!~" + type
                    new[name][i].extend(self.__get_amount(frames, amount))
        new["~~TOTAL_FRAMES~~"] = len(new[name])
        return new

class Bone(object):
    def __init__(self, startend, obj_center):
        self.start, self.end = startend

        self.center = self.get_center()

        self.obj_dif = (obj_center[0] - self.center[0],
                        obj_center[1] - self.center[1],
                        obj_center[2] - self.center[2])

        self.__base_values = (tuple(self.start), tuple(self.end), self.get_center())

        self.rotation = [0,0,0]

        self.parent = self
        self.children = []

        self.attach_parent_point = 0
        self.start_point = 0

    def get_pos(self):
        return (self.center[0] + self.obj_dif[0],
                self.center[1] + self.obj_dif[1],
                self.center[2] + self.obj_dif[2])

    def attach(self, other, opoint=0, spoint=0):
        other.parent = self
        other.attach_parent_point = opoint
        other.start_point = spoint
        self.children.append(other)

    def get_center(self):
        return (safe_div(self.start[0] + self.end[0], 2),
                safe_div(self.start[1] + self.end[1], 2),
                safe_div(self.start[2] + self.end[2], 2))

    def get_target(self, point):
        if point == 0:
            return self.start
        return self.end

    def reset(self):
        self.rotation = [0,0,0]

        self.start, self.end, self.center = self.__base_values

    def move(self, x, y, z):
        px, py, pz = self.start
        ex, ey, ez = self.end

        px += x
        ex += x
        py += y
        ey += y
        pz += z
        ez += z

        self.start = px, py, pz
        self.end = ex, ey, ez

        self.center = self.get_center()
        for i in self.children:
            i.move(x, y, z)

    def rotate(self, x, y, z):
        self.rotation[0] += x
        self.rotation[1] += y
        self.rotation[2] += z

        if self.start_point == 0:
            root = self.start
            tail = self.end
        else:
            root = self.end
            tail = self.start

        sx, sy, sz = tail
        sx -= root[0]
        sy -= root[1]
        sz -= root[2]

        if x:
            radians = math.radians(x)
            cos = math.cos(radians)
            sin = math.sin(radians)
            ox, oy, oz = float(sx), float(sy), float(sz)

            sy = (cos * oy) - (sin * oz)
            sz = (sin * oy) + (cos * oz)

        if y:
            radians = math.radians(y)
            cos = math.cos(radians)
            sin = math.sin(radians)
            ox, oy, oz = float(sx), float(sy), float(sz)

            sx = (cos * ox) - (sin * oz)
            sz = (sin * ox) + (cos * oz)

        if z:
            radians = math.radians(z)
            cos = math.cos(radians)
            sin = math.sin(radians)
            ox, oy, oz = float(sx), float(sy), float(sz)

            sx = (cos * ox) - (sin * oy)
            sy = (sin * ox) + (cos * oy)

        sx += root[0]
        sy += root[1]
        sz += root[2]

        s = (sx, sy, sz)

        if self.start_point == 0:
            dif = [s[i] - self.end[i] for i in xrange(3)]
            self.end = (sx, sy, sz)
        else:
            dif = [s[i] - self.start[i] for i in xrange(3)]
            self.start = (sx, sy, sz)

        for i in self.children:
            i.move(*dif)
            i.rotate(x, y, z)

        self.center = self.get_center()


class Limb(object):
    def __init__(self, name, gl_list, bone):
        self.name = name

        self.gl_list = gl_list

        self.bone = bone

    def attach(self, other, opoint=0, spoint=0):
        self.bone.attach(other, opoint, spoint)

    def reset(self):
        self.bone.reset()

    def rotate(self, data):
        self.bone.rotate(data[0], data[1], data[2])

    def move(self, data):
        self.bone.move(*data)

    def update(self, frame):
        name = frame[0]
        data = frame[1::]
        if "~!~" in name:
            name = name.split("~!~")
            for i in xrange(len(name)):
                n = data[i*3:(i*3)+3]
                self.update([name[i]] + n)

        else:
            if name == "ROTATE":
                self.rotate(data)
            if name == "TRANSLATE":
                self.move(data)
            if name == "RESET":
                self.reset()

    def render(self):
        glPushMatrix()
        glTranslatef(*self.bone.center)
        glRotatef(self.bone.rotation[0], 1, 0, 0)
        glRotatef(self.bone.rotation[1], 0, 1, 0)
        glRotatef(self.bone.rotation[2], 0, 0, 1)
        glCallList(self.gl_list)
        glPopMatrix()
            

class Mesh(object):
    def __init__(self, objects, faces,
                 verts, norms,
                 mtls, texcs,
                 bones, bone_connections,
                 animations,
                 swapyz=False):

        self.objects = objects
        self.faces = faces

        self.vertices = verts
        self.normals = norms

        self.materials = mtls
        self.tex_coords = texcs

        self.swapyz = swapyz

        self.bones = bones
        self.bone_connections = bone_connections

        self.limbs = self.build_limbs()

        self.animations = self.build_animations(animations)
        self.action = None
        self.frame = 0

    def reset_animation(self):
        self.frame = 0
        for i in self.limbs:
            self.limbs[i].reset()

    def update(self):
        if not self.animation_action in self.animations:
            return
        self.frame += 1
        if self.frame >= self.animations[self.animation_action].frames["~~TOTAL_FRAMES~~"]:
            self.frame = 0
            for i in self.limbs:
                self.limbs[i].reset()
        for i in self.limbs:
            i = self.limbs[i]
            if not i.name in self.animations[self.animation_action].frames:
                continue
            i.update(self.animations[self.animation_action].frames[i.name][self.frame-1])

    def build_animations(self, animations):
        new = {}
        for i in animations:
            name = i
            values = animations[i]
            new[name] = Animation(name, values)
        return new

    def build_limbs(self):
        limbs = {}
        for obj in self.objects:
            obj2 = self.objects[obj]
            gl_list = glGenLists(1)
            glNewList(gl_list, GL_COMPILE)
            glFrontFace(GL_CCW)
            for face in obj2:
                vertices, normals, texture_coords, material = face

                center = average_verts([self.vertices[i-1] for i in vertices if i > 0])
     
                mtl = self.materials[material]
                if mtl['tex']:
                    glBindTexture(GL_TEXTURE_2D, mtl['tex'])
                glColorf(*mtl['color'])
     
                glBegin(GL_POLYGON)
                for i in range(0, len(vertices)):
                    if normals[i] > 0:
                        n = self.normals[normals[i] - 1]
                        if self.swapyz:
                            n = n[0], n[2], n[1]
                        glNormal3fv(n)
                    if texture_coords[i] > 0:
                        glTexCoord2fv(self.texcoords[texture_coords[i] - 1])
                    v = self.vertices[vertices[i] - 1]
                    if self.swapyz:
                        v = v[0], v[2], v[1]

                    v = v[0] - center[0], v[1] - center[1], v[2] - center[2]
                    glVertex3fv(v)
                glEnd()
            glEndList()

            if obj in self.bones:
                bone = Bone(self.bones[obj], center)
                limbs[obj] = Limb(obj, gl_list, bone)

        for i in self.bone_connections:
            limbs[i[0]].attach(limbs[i[1]].bone, i[2], i[3])

        return limbs

    def render(self, pos, rotation=(0,0,0)):
        glPushMatrix()
        glTranslatef(*pos)
        glRotatef(rotation[0], 1, 0, 0)
        glRotatef(rotation[1], 0, 1, 0)
        glRotatef(rotation[2], 0, 0, 1)
        for i in self.limbs:
            self.limbs[i].render()
        glPopMatrix()
        return
