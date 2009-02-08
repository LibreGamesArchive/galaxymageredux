"""
pyggle.misc
This library (PYGGEL) is licensed under the LGPL by Matthew Roe and PYGGEL contributors.

The misc module contains various functions and classes that don't fit anywhere else.
"""

from include import *
import image, view, data, math3d

import random

def randfloat(a, b):
    """Returns a random floating point number in range(a,b)."""
    a = int(a*100000000)
    b = int(b*100000000)
    x = random.randint(a, b)
    return x * 0.00000001

def create_empty_texture(size=(2,2), color=(1,1,1,1)):
    """Create an empty data.Texture
       size must be a two part tuple representing the pixel size of the texture
       color must be a four-part tuple representing the (RGBA 0-1) color of the texture"""
    i = pygame.Surface(size)
    if len(color) == 4:
        r, g, b, a = color
    else:
        r, g, b = color
        a = 1
    r *= 255
    g *= 255
    b *= 255
    a *= 255
    i.fill((r,g,b,a))
    return data.Texture(i)

def create_empty_image(size=(2,2), color=(1,1,1,1)):
    """Same as create_empty_texture, except returns an image.Image instead"""
    i = pygame.Surface(size)
    if len(color) == 3:
        color = color + (1,)
    i.fill((255,255,255,255))
    return image.Image(i, colorize=color)

def create_empty_image3d(size=(2,2), color=(1,1,1,1)):
    """Same as create_empty_texture, except returns an image.Image3D instead"""
    i = pygame.Surface(size)
    if len(color) == 3:
        color = color + (1,)
    i.fill((255,255,255,255))
    return image.Image3D(i, colorize=color)

class ObjectGroup(object):
    """A simple Group object for storing a lot of similar objects in."""
    def __init__(self):
        """Create the group."""
        self._objects = []

    def __iter__(self):
        """Return an iteration object to iterate over all objects in the group."""
        return iter(self._objects)

    def __len__(self):
        """Return the size of the group."""
        return len(self._objects)

    def add(self, o):
        """Add object "o" to group."""
        self._objects.append(o)

    def remove(self, o):
        """Remove object "o" from group."""
        if o in self._objects:
            self._objects.remove(o)

class ObjectInstance(object):
    """An instance of a group of objects."""
    def __init__(self, groups):
        """Create the instance.
           groups are the ObjectGroup's this instance belongs to."""
        for g in groups:
            g.add(self)
        self._groups = groups

    def kill(self):
        """Kill the instance, removes from all groups."""
        for g in self._groups:
            g.remove(self)

    def update(self):
        """Update the instance."""
        pass

    def alive(self):
        """Return whether or not the object is alive."""
        l = []; [l.extend(i) for i in self._groups]
        return self in l

class StaticObjectGroup(object):
    """A class that takes a list of renderable objects (that won't ever change position, rotation, etc.
           This includes Image3D's - as they require a dynamic look-up of the camera to billboard correctly)
       and compiles them into a single data.DisplayList so that rendering is much faster."""
    def __init__(self, objects=[]):
        """Create the group.
           objects must be a list of renderable objects"""
        self.objects = objects
        self.gl_list = data.DisplayList()

        self.visible = True
        self.pos = (0,0,0)

        self.compile()

    def add_object(self, obj):
        """Add an object to the group - if called then group.compile() must be called afterwards, to recreate the display list"""
        self.objects.append(obj)

    def compile(self):
        """Compile everything into a data.DisplayList"""
        self.gl_list.begin()
        for i in self.objects:
            i.render()
        self.gl_list.end()

    def render(self, camera=None):
        """Render the group.
           camera should be None or the camera the scene is using - only here for compatability"""
        self.gl_list.render()

    def get_pos(self):
        """Return the position of the mesh"""
        return self.pos

def save_screenshot(filename):
    """Save a screenshot to filename"""
    pygame.image.save(pygame.display.get_surface(), filename)
