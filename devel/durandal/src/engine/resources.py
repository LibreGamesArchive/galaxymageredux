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

# Disregard for the moment

import sys

class Map:
    def __init__(self, name):
        # then lines separated by blank lines for each Abstract Map Square
        try:
            mapLines = open("data/maps/" + name, 'r').read().split("\n")
        except:
            print "map does not exist: " + name
            sys.exit()

        width = mapLines[0]
        height = mapLines[1]

        entities = mapLines[3:]

        print eList

m = Map("grove")
