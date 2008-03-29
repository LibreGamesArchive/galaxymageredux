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
                caption='Redux 0.1-alpha1')

        # Initialize Opengl state
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glClearColor(*cnormalize(black))

        # Set up scene.
        self.scene = scene.IntroScene()

        # Creat fps display
        self.fps_display = pyglet.clock.ClockDisplay()

        # Schedule game updates
        pyglet.clock.schedule_interval(self.update, 1/60.)

    def on_draw(self):
        self.clear()
        self.scene.draw()
        if config.fps:
            self.fps_display.draw()

    def update(self, dt):
        self.scene.update(dt)
        reactor.resume()

    def quit(self):
        reactor.stop()
        pyglet.app.exit()

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.ESCAPE:
            self.quit()


# ---------------------------------------------------------------------------
def release():
    reactor.callLater(0, release)
    reactor.release()
window = Redux()
reactor.callLater(0, release)
reactor.run()
pyglet.app.run()
