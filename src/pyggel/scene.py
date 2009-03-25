"""
pyggle.scene
This library (PYGGEL) is licensed under the LGPL by Matthew Roe and PYGGEL contributors.

The scene module contains classes used to represent an entire group of renderable objects.
"""

from include import *
import camera, view, picker, misc
from light import all_lights

class Tree(object):
    """A simple class used to keep track of all objects in a scene."""
    def __init__(self):#, hs, ps):
        """Create the Tree."""
        self.render_3d = []
        self.render_3d_blend = []
        self.render_2d = []
        self.render_3d_always = []
        self.skybox = None
        self.lights = []

        self.pick = picker.Group()

class Scene(object):
    """A simple scene class used to store, render, pick and manipulate objects."""
    def __init__(self):
        """Create the scene."""
        self.graph = Tree()

        self.render2d = True
        self.render3d = True

    def render(self, camera=None):
        """Render all objects.
           camera must no or the camera object used to render the scene"""
        view.set3d()
        my_lights = list(all_lights)
        if self.graph.skybox and camera:
            self.graph.skybox.render(camera)
        if self.render3d:
            if camera:
                camera.push()
            for i in self.graph.lights:
                i.gl_light = my_lights.pop()
                i.shine()
            glEnable(GL_ALPHA_TEST)
            for i in self.graph.render_3d:
                if i.visible: i.render(camera)
            glDisable(GL_ALPHA_TEST)
            glDepthMask(GL_FALSE)
            for i in self.graph.render_3d_blend:
                if i.visible: i.render(camera)
            glDepthMask(GL_TRUE)
            glDisable(GL_DEPTH_TEST)
            for i in self.graph.render_3d_always:
                if i.visible: i.render(camera)
            glEnable(GL_DEPTH_TEST)

            for i in self.graph.lights:
                i.hide()
            if camera:
                camera.pop()

        if self.render2d:
            view.set2d()
            glPushMatrix()
            rx = 1.0 * view.screen.screen_size[0] / view.screen.screen_size_2d[0]
            ry = 1.0 * view.screen.screen_size[1] / view.screen.screen_size_2d[1]
            glScalef(rx, ry, 1)
            glDisable(GL_LIGHTING)
            for i in self.graph.render_2d:
                if i.visible: i.render()
            if view.screen.lighting:
                glEnable(GL_LIGHTING)
            glPopMatrix()

    def add_2d(self, ele):
        """Add a 2d object or list of objects to the scene."""
        if not hasattr(ele, "__iter__"):
            ele = [ele]
        for i in ele:
            self.graph.render_2d.append(i)
            i.scene = self

    def remove_2d(self, ele):
        """Remove a 2d object from the scene."""
        self.graph.render_2d.remove(ele)

    def add_3d(self, ele):
        """Add a 3d, non-blended, depth-tested object or list of objects to the scene."""
        if not hasattr(ele, "__iter__"):
            ele = [ele]
        for i in ele:
            self.graph.render_3d.append(i)
            self.graph.pick.add_obj(i)

    def remove_3d(self, ele):
        """Remove a 3d object from the scene."""
        self.graph.render_3d.remove(ele)
        self.graph.pick.rem_obj(ele)

    def add_3d_blend(self, ele):
        """Add a 3d, blended, depth-tested object or list of objects to the scene."""
        if not hasattr(ele, "__iter__"):
            ele = [ele]
        for i in ele:
            self.graph.render_3d_blend.append(i)
            self.graph.pick.add_obj(i)

    def remove_3d_blend(self, ele):
        """Remove a 3d blended object from the scene."""
        self.graph.render_3d_blend.remove(ele)
        self.graph.pick.rem_obj(ele)

    def add_3d_always(self, ele):
        """Add a 3d, blended, non-depth-tested (always visible) object or list of objects to the scene."""
        if not hasattr(ele, "__iter__"):
            ele = [ele]
        for i in ele:
            self.graph.render_3d_always.append(i)

    def remove_3d_always(self, ele):
        """Remove a 3d always visible obejct from the scene."""
        self.graph.render_3d_always.remove(ele)

    def add_skybox(self, ele=None):
        """Add a Skybox or Skyball object to the scene.
           If None is given, disables skybox."""
        self.graph.skybox = ele

    def add_light(self, light):
        """Add a light to the scene."""
        if len(self.graph.lights) < 8:
            self.graph.lights.append(light)
        else:
            raise ValueError("Too many Lights - max 8")

    def remove_light(self, light):
        if light in self.graph.lights:
            self.graph.lights.remove(light)

    def pick(self, mouse_pos, camera=None):
        """Run picker and return which object(s) are hit in the 3d and 3d_blend groups, 3d_always objects won't pick!!!
           mouse_pos is the position of the mouse on screen
           camera is the camera used to render the scene
           Returns picked object or None"""
        view.set3d()

        glDisable(GL_LIGHTING)
        glEnable(GL_ALPHA_TEST)
        h = self.graph.pick.pick(mouse_pos, camera)
        glDisable(GL_ALPHA_TEST)
        glEnable(GL_LIGHTING)
        if h:
            hit, depth = h
        else:
            hit = None

        view.clear_screen()
        return hit
