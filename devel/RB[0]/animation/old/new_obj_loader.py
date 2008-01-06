import pygame
from OpenGL.GL import *
import os
import texture

class Limb(object):
    def __init__(self, gl_list):
        self.gl_list = gl_list

        self.rotation = (0, 0, 0)
        self.pos = (0, 0, 0)
        self.stretch = 0

    def render(self, pos):
        glPushMatrix()
        glTranslatef(*pos)
        glTranslatef(*self.pos)
        glRotatef(1, self.rotation[0], 0, 0)
        glRotatef(1, 0, self.rotation[1], 0)
        glRotatef(1, 0, 0, self.rotation[2])
        glScalef(0, self.stretch, 0)
        glCallList(self.gl_list)
        glPopMatrix()

        return None

class Mesh(object):
    def __init__(self, vertices=[], normals=[], texcoords=[], faces=[],
                 objects=[], materials={}, swapyz = False):

        self.vertices = vertices
        self.normals = normals
        self.texcoords = texcoords
        self.faces = faces

        self.materials = materials

        self.limbs = {}

        for o in objects:
            gl_list = glGenLists(1)
            glNewList(gl_list, GL_COMPILE)
            glFrontFace(GL_CCW)
            for face in objects[o]["faces"]:
                vertices, normals, texture_coords, material = face
     
                mtl = self.materials[material]
                if 'map_Kd' in mtl:
                    # use diffuse texmap
                    glBindTexture(GL_TEXTURE_2D, mtl['map_Kd'])
                glColorf(*mtl['Kd'])
     
                glBegin(GL_POLYGON)
                for i in range(0, len(vertices)):
                    if normals[i] > 0:
                        n = self.normals[normals[i] - 1]
                        if swapyz:
                            n = n[0], n[2], n[1]
                        glNormal3fv(n)
                    if texture_coords[i] > 0:
                        glTexCoord2fv(self.texcoords[texture_coords[i] - 1])
                    v = self.vertices[vertices[i] - 1]
                    if swapyz:
                        v = v[0], v[2], v[1]
                    glVertex3fv(v)
                glEnd()
            glEndList()
            self.limbs[o] = Limb(gl_list)

    def render(self, pos):
        for i in self.limbs:
            self.limbs[i].render(pos)

def getMTL(filename):
    contents = {}
    mtl = {}
    cur_cont = None
    for line in open(filename, "r"):
        if line.startswith('#'): continue

        values = line.split()
        if not values: continue
        if values[0] == "newmtl":
            if mtl:
                contents[cur_cont] = mtl
                mtl = {}
            mtl = {}
            contents[values[1]] = {}
            cur_cont = values[1]
        elif mtl == None:
            raise ValueError, "mtl file doesn't start with newmtl statement"
        elif values[0] == "map_Kd":
            path = os.path.join(os.path.split(filename)[0], values[1])
            tex = texture.image(path)
            texid = tex.image
            mtl[values[0]] = texid
        elif values[0] == "Kd":
            mtl[values[0]] = map(float, values[1:])
    if mtl:
        contents[cur_cont] = mtl
    return contents

def getOBJ(filename):
    verts = []
    norms = []
    texcs = []
    faces = []

    material = None
    mtl = {}

    objects = {}
    cur_object = ""

    for line in open(filename, "r"):
        if line.startswith('#'): continue
        values = line.split()
        if not values: continue

        if values[0] == 'v':
            v = map(float, values[1:4])
            verts.append(v)
            objects[cur_object]["verts"].append(v)
        elif values[0] == 'vn':
            v = map(float, values[1:4])
            norms.append(v)
            objects[cur_object]["norms"].append(v)
        elif values[0] == 'vt':
            texcs.append(map(float, values[1:3]))
            objects[cur_object]["texcs"].append(map(float, values[1:3]))
        elif values[0] in ('usemtl', 'usemat'):
            material = values[1]
        elif values[0] == 'mtllib':
            path = os.path.join(os.path.split(filename)[0], values[1])
            n = getMTL(path)
            for i in n:
                mtl[i] = n[i]
        elif values[0] == 'f':
            f = []
            tc = []
            n = []
            for v in values[1:]:
                w = v.split('/')
                f.append(int(w[0]))
                if len(w) >= 2 and len(w[1]) > 0:
                    tc.append(int(w[1]))
                else:
                    tc.append(0)
                if len(w) >= 3 and len(w[2]) > 0:
                    n.append(int(w[2]))
                else:
                    n.append(0)
            faces.append((f, n, tc, material))
            objects[cur_object]["faces"].append((f, n, tc, material))
        elif values[0] == "o":
            cur_object = values[1]
            objects[cur_object] = {"verts":[],
                                   "norms":[],
                                   "texcs":[],
                                   "faces":[]}
    return (verts, norms, texcs, faces, objects, mtl)

##def safe_div(x, y):
##    if x and y:
##        return x / y
##    return 0
##
##def get_middle(objects):
##    mx, my, mz = 0, 0, 0
##    num = 0
##    for i in objects:
##        mx += i[0]
##        my += i[1]
##        mz += i[2]
##        num += 1
##    return (safe_div(mx, num),
##            safe_div(my, num),
##            safe_div(mz, num))
##
##def center_objects(verts, norms, texcs, faces, objects, mtl):
##    for o in objects:
##        oo = objects[o]
##        middle = get_middle(oo["verts"])
##        for i in oo["verts"]:
##            x1, y1, z1 = i
##            x2, y2, z2 = verts[verts.index(i)]
##
##            x1 -= middle[0]
##            x2 -= middle[0]
##            y1 -= middle[1]
##            y2 -= middle[1]
##            z1 -= middle[2]
##            z2 -= middle[2]
##
##            verts[verts.index(i)] = x2, y2, z2
##            i = x1, y1, z1
##
##        middle = get_middle(oo["norms"])
##        for i in oo["norms"]:
##            x1, y1, z1 = i
##            x2, y2, z2 = norms[norms.index(i)]
##
##            x1 -= middle[0]
##            x2 -= middle[0]
##            y1 -= middle[1]
##            y2 -= middle[1]
##            z1 -= middle[2]
##            z2 -= middle[2]
##
##            norms[norms.index(i)] = x2, y2, z2
##            i = x1, y1, z1
##
##    return verts, norms, texcs, faces, objects, mtl
        

def load_obj(filename, swapyz=False):
##    meshes = []
##    objects, mtl = getOBJ(filename)
##    for i in objects:
##        i = objects[i]
##        meshes.append(Mesh(i["verts"], i["norms"], i["texcs"], i["faces"], mtl, swapyz))
##    return meshes
##    return Mesh(* (center_objects(*getOBJ(filename)) + (swapyz,) ))
    return Mesh(*(getOBJ(filename) + (swapyz,)))
    
