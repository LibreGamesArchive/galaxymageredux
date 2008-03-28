#!/usr/bin/env python

# LICENSE:
#
# Copyright (c) 2007-2008 A. Joseph Hager and Redux contributors.
#
# Redux is free software; you can redistribute it and/or modify it under the
# terms of version 2 of the GNU General Public License, as published by the
# Free Software Foundation.
# 
# Redux is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
# 
# You should have received a copy of the GNU General Public License along
# with Redux; if not, write to the Free Software Foundation, Inc., 51 Franklin
# Street, Fifth Floor, Boston, MA 02110-1301, USA.


# Add our src directory to the path.
import sys
sys.path.insert(0, 'src')

import pyglet
pyglet.options['debug_gl'] = False
from pyglet.gl import *
from network import pausingreactor; pausingreactor.install()
from twisted.internet import reactor

from graphics import scene
from graphics.colors import *
from network.basic import Client
import config

class Redux(pyglet.window.Window):
    def __init__(self):
        pyglet.window.Window.__init__(self, config.width, config.height,
                caption='Redux 0.1')

        # Initialize Opengl state
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glClearColor(*cnormalize(black))

        # Setup scene
        self.scenes = []
        self.scene = None
        self.next_scene = None
        self.push_scene(self.scene)
        self._set_scene(scene.IntroScene(self))

        # Creat fps display
        self.fps_display = pyglet.clock.ClockDisplay()

        # Schedule game updates
        pyglet.clock.schedule_interval(self.update, 1/60.)

    def _set_scene(self, scene):
        self.next_scene = None
        if self.scene:
            self.scene.exit()
        self.scene = scene
        scene.enter()

    def push_scene(self, scene):
        self.next_scene = scene
        self.scenes.append(self.scene)

    def pop_scene(self):
        self.next_scene = self.scenes.pop()

    def replace_scene(self, scene):
        self.next_scene = scene

    def on_draw(self):
        self.clear()
        self.scene.draw()
        if config.fps:
            self.fps_display.draw()

    def update(self, dt):
        if self.next_scene:
            self._set_scene(self.next_scene)

        if not self.scenes:
            reactor.stop()
            pyglet.app.exit()

        self.scene.update(dt)
        reactor.resume()

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.ESCAPE:
            self.pop_scene()


# ---------------------------------------------------------------------------
def release():
    reactor.callLater(0, release)
    reactor.release()
window = Redux()
reactor.callLater(0, release)
reactor.run()
pyglet.app.run()
