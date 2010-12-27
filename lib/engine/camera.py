from include import *

"""
Camera should have a target view position and an offset position.
Use transforms to point the camera at target.
Rotating camera should move it's offset position in relation to it's target.
"""


class Camera(object):
    def __init__(self, target=(0,0,0), offset=(0,0,-1)):

        self.offset_pos = pos
        self.target_pos = target

    def rotate_view(self, xyz):
        #TODO, rotate offset in relation to target

    def move_offset(self, xyz):
        #TODO, move offset

    def push(self):
        #TODO: setup camera projection matrix for rendering

    def pop(self):
        #TODO: pop camera projection matrix

    def push_facing_matrix(self):
        #TODO: force objects to be pointed right at camera
