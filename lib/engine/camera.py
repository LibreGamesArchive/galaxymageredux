from include import *

"""
Camera should have a target view position and an offset position.
Use transforms to point the camera at target.
Rotating camera should move it's offset position in relation to it's target.

Make a camera class with a real position (we may want to do some stuff with 
that later) that looks at a tile we are on.
Camera should be able to interpolate to a position cleanly/quickly.
Perhaps do a simple camera that just points at something and moves away - no 
math needed just works easily, we can do fancier stuff at a later point!
"""


class Camera(object):
    def __init__(self, target=(0,0,0), offset=(0,0,-1)):
        self.offset_pos = offset
        self.target_pos = target

    def rotate_view(self, xyz):
        #TODO, rotate offset in relation to target
        pass

    def move_offset(self, xyz):
        #TODO, move offset
        pass

    def push(self):
        #TODO: setup camera projection matrix for rendering
        pass

    def pop(self):
        #TODO: pop camera projection matrix
        pass

    def push_facing_matrix(self):
        #TODO: force objects to be pointed right at camera
        pass
