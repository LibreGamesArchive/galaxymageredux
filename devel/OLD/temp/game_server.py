# LICENSE:
#
# Copyright (c) 2007 GalaxyMage Redux contributors.
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

from twisted.spread import pb
from twisted.internet import reactor
from network.basic import Server
from network import realm

class GameServer(Server):
    def __init__(self):
        Server.__init__(self)
        self.type = 'game'
        self.active_client = 0 # Whose turn it is, one unit per client for now

        # Simplified from RB's test_map.py for now..
        test_map = [[None, None], [None, None]] # A list of units' positions
        self.game_map = test_map

        reactor.callLater(0, self.gameLoop) # Start game loop

    def join(self, avatar):
        """Override base class method to find an empty spot for the new player."""
        Server.join(self, avatar)

        # Make new unit for avatar
        unit = Unit(avatar)
        x, y = self._findEmptyTile()
        if x == None:
            print 'Too many clients for the map!'
            return

        unit.position = (x, 5, y)
        self.game_map[x][y] = unit
        self.remoteAll('updateUnits', self._getUnitPositions()) # update clients

    def leave(self, avatar):
        """Override base class method to update the map when players leave."""
        Server.leave(self, avatar)

        unit, x, y = self._findUnit(avatar)
        if unit:
            self.game_map[x][y] = None
        self.remoteAll('updateUnits', self._getUnitPositions()) # update clients

    def gameLoop(self):
        """Main loop in the server. Manages the game engine and state. Informs 
        clients of anything necessary."""
        # Not necessary at the moment
        #reactor.callLater(0, self.gameLoop) # Keep the loop running

    def requestMove(self, avatar, unit_id, position):
        """The caller requests to move his unit to this position."""
        print "Avatar %s requested a move to" % self.avatars[self.active_client].name,
        print "%s, %s, %s" % position

        # Check that this request came from the active client
        if self.active_client != self.avatars.index(avatar):
            print "Sorry, it is %s's turn" % self.avatars[self.active_client].name
            return # It's not your turn, ignore

        # Check for an empty destination
        if self.game_map[position[0]][position[2]] == None:
            unit, x, y = self._findUnit(avatar)
            if unit == None:
                return

            unit.position = position # update game world position
            self.game_map[x][y] = None # remove old map index
            self.game_map[position[0]][position[2]] = unit # set new map index
            self.remoteAll('updateUnits', self._getUnitPositions()) # update clients
            self.updateTurn() # client used his turn

    def updateTurn(self):
        """Simple function to move to the next client's turn."""
        if self.active_client < len(self.avatars)-1:
            self.active_client += 1
        else:
            self.active_client = 0

    def _findUnit(self, avatar):
        """Finds the unit belonging to the avatar and it's indices in the map."""
        for i in range(len(self.game_map)): # width
            for j in range(len(self.game_map[0])): # height
                unit = self.game_map[i][j]
                if unit and unit.owner == avatar:
                    return unit, i, j

        return None, None, None # not found

    def _findEmptyTile(self):
        """Finds an empty tile for spawning new units."""
        for i in range(len(self.game_map)): # width
            for j in range(len(self.game_map[0])): # height
                if self.game_map[i][j] == None:
                    return i, j

        return None, None

    def _getUnitPositions(self):
        """Gets all the positions of units for updating clients."""
        positions = []
        for i in range(len(self.game_map)): # width
            for j in range(len(self.game_map[0])): # height
                unit = self.game_map[i][j]
                if unit:
                    positions.append(unit.position)

        return positions

## _Very_ simple class just for testing purposes
class Unit(object):
    def __init__(self, owner):
        self.owner = owner
        self.position = (0, 0, 0)

s = GameServer()
r = realm.Realm(44444, s)
r.start()
