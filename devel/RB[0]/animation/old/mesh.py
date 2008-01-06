"""This module is part of the PygLibsX library.
It is licensed under an open-source, make-shift license by Matthew Roe.
That will change when it is more complete and I know what I want ot do with it."""

import math
import math3d

class MeshPart(object):
    def __init__(self, mesh, bone):
        self.mesh = mesh
        self.bone = bone

        self.center = (0, 0, 0)

    def check_collision(self, other):
        self.get_center()
        return self.mesh.collision_geom.check_collision(other.mesh.collision_geom)

    def get_center(self):
        x = (self.bone.start.x + self.bone.end.x) / 2
        y = (self.bone.start.y + self.bone.end.y) / 2
        z = (self.bone.start.z + self.bone.end.z) / 2
        self.center = (x, y, z)
        self.mesh.collision_box.pos = math3d.Vector(*self.center)
        return self.center

    def render(self):
        self.mesh.render(self.get_center(), self.bone.rot_angle)
        return None

class Bone(object):
    def __init__(self, start, end):

        self.start = math3d.Vector(*start)
        self.end = math3d.Vector(*end)

        self.rot_angle = [0, 0, 0]

        self.parent = None
        self.parent_attach_point = 0 #0=End, 1=Start

        self.children = []

    def pick_place(self, place):
        if place == 0:
            return self.end
        return self.start

    def attach(self, bone, attach_to="End"):
        self.children.append(bone)
        bone.parent = self
        if attach_to == "End" or attach_to == "end":
            bone.parent_attach_point = 0
        elif attach_to == "Start" or attach_to == "start":
            bone.parent_attach_point = 1
        else:
            bone.parent_attach_point = attach_to

        bone.move_static(self.pick_place(bone.parent_attach_point))
        return None

    def move_static(self, vec):
        x, y, z = self.start.x, self.start.y, self.start.z
        bx, by, bz = vec.x, vec.y, vec.z

        difx = bx - x
        dify = by - y
        difz = bz - z

        self.start.add(math3d.Vector(difx, dify, difz))
        self.end.add(math3d.Vector(difx, dify, difz))
        for i in self.children:
            i.move_static(self.pick_place(i.parent_attach_point))
        return None

    def rotate_around_me(self, x, y, z, other):
        a = self.pick_place(other.parent_attach_point)
        b = self.pick_place(not other.parent_attach_point)

        a.rotate(x, y, z, (b.x, b.y, b.z))
        for i in self.children:
            i.move_static(self.pick_place(i.parent_attach_point))
            i.rotate_around_me(x, y, z, self)

        self.rot_angle[0] += x
        self.rot_angle[1] += y
        self.rot_angle[2] += z
        return None

    def rotate_self(self, x, y, z):
        self.end.rotate(x, y, z, (self.start.x, self.start.y, self.start.z))
        for i in self.children:
            i.move_static(self.end)
            i.rotate_self(x, y, z)
        self.rot_angle[0] += x
        self.rot_angle[1] += y
        self.rot_angle[2] += z
        return None

    def move(self, x, y, z):
        """rotate parents attach point by x, y, z and rotate reverse for self.start"""
        self.end.rotate(x, y, z, (self.start.x, self.start.y, self.start.z))
        for i in self.children:
            i.move_static(self.pick_place(i.parent_attach_point))
            i.rotate_around_me(x, y, z, self)
        self.rot_angle[0] -= x
        self.rot_angle[1] -= y
        self.rot_angle[2] -= z
        return None

    def shift(self, x, y, z):
        if self.parent:
            self.parent.move(x, y, z)
            self.move_static(self.parent.pick_place(self.parent_attach_point))
            self.rotate_self(-x, -y, -z)
        else:
            self.move_static(math3d.Vector(x, y, z))
        return None

    def render(self):
        if self.mesh:
            self.mesh.render(self.get_center())
            

a = Bone((4, 4, 4), (4, 0, 4))
