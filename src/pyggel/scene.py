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

        self.pick_3d = picker.Group()
        self.pick_3d_blend = picker.Group()
        self.pick_3d_merged = picker.Group()
        self.pick_3d_always = picker.Group()

class PickResult(object):
    """A simple class for storing the results of a picking operation."""
    def __init__(self, hits, depths):
        """Create the result.
           hits must be a three part tuple representing the topmost object picked from each render_3d* group in the scene Tree
           depths must be a three part tuple representing the depths of the hits"""
        self.hit3d, self.hit3d_blend, self.hit3d_always = hits
        self.dep3d, self.dep3d_blend, self.dep3d_always = depths

        a, b, c = depths
        if a == None: a = 100
        if b == None: b = 100
        if c == None: c = 100
        depths = [a, b, c]

        self.hit = hits[depths.index(min(depths))]

class Scene(object):
    """A simple scene class used to store, render, pick and manipulate objects."""
    def __init__(self):
        """Create the scene."""
        self.graph = Tree()

        self.render2d = True
        self.render3d = True

    def render(self, camera):
        """Render all objects.
           camera must be the camera object used to render the scene"""
        view.set3d()
        my_lights = list(all_lights)
        if self.graph.skybox:
            self.graph.skybox.render(camera)
        if self.render3d:
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
            camera.pop()

        if self.render2d:
            view.set2d()
            glDisable(GL_LIGHTING)
            for i in self.graph.render_2d:
                if i.visible: i.render()
            if view.screen.lighting:
                glEnable(GL_LIGHTING)

    def add_2d(self, ele):
        """Add a 2d object to the scene."""
        self.graph.render_2d.append(ele)
        ele.scene = self

    def remove_2d(self, ele):
        """Remove a 2d object from the scene."""
        self.graph.render_2d.remove(ele)

    def add_3d(self, ele):
        """Add a 3d, non-blended, depth-tested object to the scene."""
        self.graph.render_3d.append(ele)
        self.graph.pick_3d.add_obj(ele)

    def remove_3d(self, ele):
        """Remove a 3d object from the scene."""
        self.graph.render_3d.remove(ele)
        self.graph.pick_3d.rem_obj(ele)

    def add_3d_blend(self, ele):
        """Add a 3d, blended, depth-tested object to the scene."""
        self.graph.render_3d_blend.append(ele)
        self.graph.pick_3d_blend.add_obj(ele)

    def remove_3d_blend(self, ele):
        """Remove a 3d blended object from the scene."""
        self.graph.render_3d_blend.remove(ele)
        self.graph.pick_3d_blend.rem_obj(ele)

    def add_3d_always(self, ele):
        """Add a 3d, blended, non-depth-tested (always visible) object to the scene."""
        self.graph.render_3d_always.append(ele)
        self.graph.pick_3d_always.add_obj(ele)

    def remove_3d_always(self, ele):
        """Remove a 3d always visible obejct from the scene."""
        self.graph.render_3d_always.remove(ele)
        self.graph.pick_3d_always.rem_obj(ele)

    def add_skybox(self, ele):
        """Add a Skybox or Skyball object to the scene."""
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

    def pick(self, mouse_pos, camera):
        """Run picker and return which object(s) are hit in each render_3d* group in the scene.
           mouse_pos is the position of the mouse on screen
           camera is teh camera used to render the scene
           Returns a PickResult object"""
        view.set3d()

        glEnable(GL_ALPHA_TEST)
        h1 = self.graph.pick_3d.pick(mouse_pos, camera)
        glDisable(GL_ALPHA_TEST)

        glDepthMask(GL_FALSE)
        h2 = self.graph.pick_3d_blend.pick(mouse_pos, camera)
        glDepthMask(GL_TRUE)

        glDisable(GL_DEPTH_TEST)
        h3 = self.graph.pick_3d_always.pick(mouse_pos, camera)
        glEnable(GL_DEPTH_TEST)

        hits = []
        depths = []

        if h1:
            hits.append(h1[0])
            depths.append(h1[1])
        else:
            hits.append(None)
            depths.append(None)

        if h2:
            hits.append(h2[0])
            depths.append(h2[1])
        else:
            hits.append(None)
            depths.append(None)

        if h3:
            hits.append(h3[0])
            depths.append(h3[1])
        else:
            hits.append(None)
            depths.append(None)

        view.clear_screen()
        return PickResult(hits, depths)
