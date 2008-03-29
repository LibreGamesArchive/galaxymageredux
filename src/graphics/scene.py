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


pyglet.resource.path.extend(['data/core/font',
                             'data/core/image',
                             'data/core/map',
                             'data/core/model',
                             'data/core/music',
                             'data/core/sfx',
                             'data/core/music'])
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


class IntroScene(Scene):
    def __init__(self, window):
        Scene.__init__(self, window)

        # Create underlays and overlays.
        self.menu = overlay.Menu('Redux', 400, 400, font_name='Quark')
        self.menu.add_item(overlay.MenuItem('Start Game', self.start_game))
        self.menu.add_item(overlay.MenuItem('Join Game', self.join_game))
        self.menu.add_item(overlay.MenuItem('Options', lambda: None))
        self.menu.add_item(overlay.MenuItem('About', lambda: None))
        self.menu.add_item(overlay.MenuItem('Quit', self.window.pop_scene))
        #self.menu.add_item(overlay.ToggleMenuItem('Vsync', self.window.vsync,
        #                                          self.window.set_vsync))
        self.overlays.append(self.menu)

        # Set one of them active.
        self.active = self.menu

    def start_game(self):
        self.window.push_scene(LocalGameScene(self.window))

    def join_game(self):
        self.window.push_scene(NetworkGameScene(self.window, 'localhost', 44444))


class LocalGameScene(Scene, Client):
    def __init__(self, window):
        Scene.__init__(self, window)
        # Temporary hack to minimize port conflicts.
        port = random.randint(1025, 100000)
        Client.__init__(self, 'localhost', 44444, config.user)

        # Create and start server.
        self.realm = Realm(44444, Server())
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


class NetworkGameScene(Scene, Client):
    def __init__(self, window, host, port):
        Scene.__init__(self, window)
        Client.__init__(self, host, port, config.user)

        # Create and start server.
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
