# LICENSE:
#
# Copyright (c) 2007 Brandon Barnes and GalaxyMage Redux contributors.
#
# GalaxyMage Redux is free software; you can redistribute it and/or 
# modify it under the terms of version 2 of the GNU General Public 
# License, as published by the Free Software Foundation.
# 
# GalaxyMage Redux is distributed in the hope that it will be useful, 
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with GalaxyMage Redux; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.

from network.basic import Client

from gui.display import Display
from gui.scene import Scene
from gui.director import Director

from twisted.internet import reactor


class OpenGLClient(Client):
    def __init__(self, host, port, user, director):
        Client.__init__(self, host, port, user)
        self.director = director
        
    def remote_turnQuad():
        pass
    
    def connected(self, avatar):
        print "yo yo"
        self.avatar = avatar
        self.update()

    def update(self):
        if self.director.action():
            reactor.callLater(0, self.update)
        else:
            reactor.stop()
        
user = raw_input("What is your name? ")
director = Director(Display(800, 600), Scene())
client = OpenGLClient("localhost", 44444, user, director).connect()
