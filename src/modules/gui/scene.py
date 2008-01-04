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

import qgl


class Scene(object):
    def __init__(self):
        # Set up the traversal visitors
        self.compiler = qgl.render.Compiler()
        self.renderer = qgl.render.Render()
        self.picker = qgl.render.Picker()

        # Add a root node and 2d/3d viewports
        self.root = qgl.scene.Root()
        self.background = qgl.scene.PerspectiveViewport()
        self.foreground = qgl.scene.OrthoViewport()
        self.root.add(self.background, self.foreground)

        # Compile the graph to OpenGL calls
        self.build()

    def addForeground(self, node):
        self.foreground.add(node)
        self.build()

    def addBackground(self, node):
        self.background.add(node)
        self.build()

    def build(self):
        self.root.accept(self.compiler)

    def film(self):
        self.root.accept(self.renderer)

    def pick(self, position):
        self.picker.set_position(position)
        self.root.accept(self.picker)
        for hit in self.picker.hits:
            pass 
