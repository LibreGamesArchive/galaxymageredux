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


import random

import pyglet
from pyglet.gl import *

from graphics import model, sprite3d, colors, overlay
from network.basic import Client, Server
from network.realm import Realm
import config


for datadir in config.datadirs:
            pyglet.resource.path.append(datadir)
            pyglet.resource.reindex()
pyglet.resource.add_font('quark.ttf')


class Scene(object):
    def __init__(self, window):
        self.window = window
        self.overlays = [] # 2d
        self.underlays = [] # 3d
        self.active = None

    def setup_2d(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, config.width, 0, config.height)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def setup_3d(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, float(config.width)/config.height, 0.1, 1000.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def activate(self, lay):
        self.window.pop_handlers()
        self.active = lay
        self.window.push_handlers(self.active)

    def enter(self):
        self.window.push_handlers(self.active)

    def exit(self):
        self.window.pop_handlers()
            
    def draw(self):
        self.setup_3d()
        for underlay in self.underlays:
            underlay.draw()

        self.setup_2d()
        for overlay in self.overlays:
            overlay.draw()

    def update(self, dt):
        for underlay in self.underlays:
            underlay.update(dt)
        for overlay in self.overlays:
            overlay.update(dt)


class IntroScene(Scene, Client):
    def __init__(self, window):
        Scene.__init__(self, window)
        # Temporary hack to minimize port conflicts.
        port = random.randint(1025, 10000)
        Client.__init__(self, 'localhost', port, config.user)

        # Create and start server.
        self.realm = Realm(port, Server())
        self.realm.start()
        self.connect()

        # Create underlays and overlays.
        self.menu = overlay.Menu('Redux', 400, 400, font_name='Quark')
        self.menu.add_item(overlay.MenuItem('Start Game',
                                            self.start_game,
                                            font_name='Quark'))
        self.menu.add_item(overlay.ToggleMenuItem('Vsync',
                                                  self.window.vsync,
                                                  self.window.set_vsync,
                                                  font_name='Quark'))
        self.overlays.append(self.menu)

        # Set one of them active.
        self.active = self.menu

    def start_game(self):
        self.window.push_scene(GameScene(self.window))


class GameScene(Scene, Client):
    def __init__(self, window):
        Scene.__init__(self, window)
        # Temporary hack to minimize port conflicts.
        port = random.randint(1025, 10000)
        Client.__init__(self, 'localhost', port, config.user)

        # Create and start server.
        self.realm = Realm(port, Server())
        self.realm.start()
        self.connect()

        # Create underlays and overlays.
        self.chatbox = overlay.ChatBox(10, 250, 350, 200, self.send_message, 'bottom')
        self.overlays.append(self.chatbox)

        # Set one of them active.
        self.active = self.chatbox

    # send_ = to server, message
    def send_message(self, msg):
        self.avatar.callRemote('message', msg)

    # remote_ = from server, message
    def remote_message(self, msg):
        self.chatbox.add_text(msg)
