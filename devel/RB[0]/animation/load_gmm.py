import os

import pygame
from pygame.locals import *

import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *

VERSION = "0.1rc1"

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
            bones[values[1]] = (map(float, values[2:4]),
                                map(float, values[5:7]))

        if values[0] == "cb":
            bone_connections.append([values[1], values[2], int(values[3])])

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

class AnimationAction(object):
    def __init__(self, actions):
        self.actions = actions

        self.num_frames = self.get_num_frames()

        self.comp_ani = self.get_comp_ani()

        self.current_frame = 0

    def get_comp_ani(self):
        comp = {}
        for i in self.actions:
            if not i[1] in comp:
                comp[i[1]] = []
            comp[i[1]].append([i[0], i[2], i[3]])
        return comp

    def get_num_frames(self):
        cur = 0
        for i in self.actions:
            end = i[2][1]
            if end > cur:
                cur = end
        return cur

    def make_value(self, start, end, L):
        return ((L[0] / (end - start)) * (self.current_frame - start),
                (L[1] / (end - start)) * (self.current_frame - start),
                (L[2] / (end - start)) * (self.current_frame - start))

    def get_current_frame(self, object_name):
        print object_name, self.comp_ani
        if object_name in self.comp_ani:
            cur = []
            for i in self.comp_ani[object_name]:
                if i[2][0] <= self.current_frame <= i[2][1]:
                    if i[0] == "ROTATE":
                        cur.append(["ROTATE", self.make_value(i[2][0], i[2][1], i[3])])
                    else:
                        cur.append(["TRANSLATE", self.make_value(i[2][0], i[2][1], i[3])])
            return cur
        return []

    def update(self):
        self.current_frame += 1
        if self.current_frame > self.num_frames:
            self.current_frame = 0


class Limb(object):
    def __init__(self, name, gl_list, bone):
        self.name = name
        self.gl_list = gl_list
        self.bone = bone

        self.parent = None
        self.attach_point = 0
        self.children = []

        self.position_dif = (0, 0, 0)
        self.rotation_dif = (0, 0, 0)

    def attach(self, other, point):
        other.parent = self
        other.attach_point = point
        self.children.append(other)

    def render(self):
        glPushMatrix()
        glTranslatef(*self.position_dif)
        glRotatef(1, self.rotation_dif[0], 0, 0)
        glRotatef(1, 0, self.rotation_dif[1], 0)
        glRotatef(1, 0, 0, self.rotation_dif[2])
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

        self.bones = bones
        self.bone_connections = bone_connections

        self.swapyz = swapyz

        self.animations = self.build_animations(animations)

        self.action = None

        self.limbs = self.build_limbs()

        self.build_connections()

    def update(self):
        if self.action:
            self.animations[self.action].update()

            for i in self.limbs:
                a = self.animations[self.action].get_current_frame(i)
                for x in a:
                    if x[0] == "ROTATE":
                        i.rotation_dif = x[1]
                    if x[0] == "TRANSLATE":
                        i.position_dif = x[1]
                print a

    def build_animations(self, animations):
        new = {}
        for i in animations:
            new[i] = AnimationAction(animations[i])
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
                    glVertex3fv(v)
                glEnd()
            glEndList()

            if obj in self.bones:
                limbs[obj] = Limb(obj, gl_list, self.bones[obj])
            else:
                limbs[obj] = Limb(obj, gl_list, None)
        return limbs

    def build_connections(self):
        for i in self.bone_connections:
            for o in self.limbs:
                o = self.limbs[o]
                if o.name == i[0]:
                    o.attach(self.limbs[i[1]], i[2])

    def render(self, pos=(0,0,0)):
        glPushMatrix()
        glTranslatef(*pos)
        for i in self.limbs:
            self.limbs[i].render()
        glPopMatrix()

def main():
    import core
    core.init()
    core.set3d()

    c = core.Camera()
    c.distance = 100

    l = core.Light((0,0,-15),
              (1,1,1,1),
              (1,1,1,1),
              (1,1,1,1))

    clock = pygame.time.Clock()

    for i in xrange(25):
        clock.tick(15)
        core.clear_screen()
        c.update()

        a = Mesh(*parse_file("test.gmm"))
        a.action = "rotate"
        a.render((0, 0, 25))
        a.update()
        pygame.display.flip()
main()
