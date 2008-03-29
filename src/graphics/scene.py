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

from graphics.overlay import Menu, MenuItem, ToggleMenuItem, InputMenuItem, ChatBox
from graphics.colors import *
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
    def __init__(self):
        self.window = None
        for window in pyglet.app.windows:
            self.window = window

        self.overlays = [] # 2d
        self.underlays = [] # 3d

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

    def update(self, dt):
        for underlay in self.underlays:
            underlay.update(dt)
        for overlay in self.overlays:
            overlay.update(dt)

    def draw(self):
        self.setup_3d()
        for underlay in self.underlays:
            underlay.draw()

        self.setup_2d()
        for overlay in self.overlays:
            overlay.draw()


class IntroScene(Scene):
    def __init__(self):
        Scene.__init__(self)

        # Main Menu.
        self.main_menu = Menu('Redux', 400, 400, font_name='Quark')
        self.main_menu.add_items([MenuItem('Start Game', self.start_game),
                                  MenuItem('Join Game', self.focus_join_game_menu),
                                  MenuItem('Options', self.focus_options_menu),
                                  MenuItem('Quit', self.window.quit)])

        # Join Game Menu.
        self.join_game_host = 'localhost'
        self.join_game_port = 44444
        self.join_game_menu = Menu('Start Game', 400, 400, font_name='Quark')
        self.join_game_menu.add_items([InputMenuItem('Host', self.join_game_host, self.set_join_game_host),
                                       InputMenuItem('Port', self.join_game_port, self.set_join_game_port),
                                       MenuItem('Join', self.join_game),
                                       MenuItem('Back', self.focus_main_menu)])

        # Options Menu.
        self.options_menu = Menu('Options', 400, 400, font_name='Quark')
        self.options_menu.add_items([InputMenuItem('Name', config.name, self.set_name),
                                     ToggleMenuItem('Fps', config.fps, self.set_fps),
                                     ToggleMenuItem('Vsync', self.window.vsync, self.window.set_vsync),
                                     ToggleMenuItem('Sound', config.sound, self.set_sound),
                                     MenuItem('Back', self.focus_main_menu)])

        # Set up initial scene.
        self.focus_main_menu()

    def focus_main_menu(self):
        self.set_menu(self.main_menu)

    def focus_join_game_menu(self):
        self.set_menu(self.join_game_menu)

    def focus_options_menu(self):
        self.set_menu(self.options_menu)

    def set_menu(self, menu):
        self.window.remove_handlers(*self.overlays)
        self.overlays = [menu]
        self.window.push_handlers(*self.overlays)

    def set_sound(self, value):
        config.sound = value

    def set_name(self, value):
        config.name = value

    def set_fps(self, value):
        config.fps = value

    def set_join_game_host(self, value):
        self.join_game_host = value

    def set_join_game_port(self, value):
        self.join_game_port = int(value)

    def start_game(self):
        self.window.remove_handlers(*(self.overlays + self.underlays))
        realm = Realm(44444, Server())
        realm.start()
        self.window.scene = GameScene()

    def join_game(self):
        self.window.remove_handlers(*(self.overlays + self.underlays))
        self.window.scene = GameScene(self.join_game_host, self.join_game_port)


class GameScene(Scene, Client):
    def __init__(self, host='localhost', port=44444):
        Scene.__init__(self)
        Client.__init__(self, host, port, config.name)

        # Join server.
        self.connect()

        # Chat box..
        self.chatbox = ChatBox(10, 250, 350, 200, self.send_message, 'bottom')

        # Set up initial scene.
        self.overlays = [self.chatbox]
        self.focus_chatbox()

    def focus_chatbox(self):
        self.window.push_handlers(*self.overlays)

    # send_ = to server, message
    def send_message(self, msg):
        self.avatar.callRemote('message', msg)

    # remote_ = from server, message
    def remote_message(self, msg):
        self.chatbox.add_text(msg)
