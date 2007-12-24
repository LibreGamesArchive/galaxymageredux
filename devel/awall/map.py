"""Docstring"""

import unit

class MapPanel(object):
    """Docstring"""
    
    
    def __init__(self, elevation=-1):
        self.material = None #TODO: Implement material later
        
        # The elevation at this panel
        # TODO: How does this work with multiple corners?
        self.elevation = elevation
        
        # The depth of the terrain at this panel.
        # Mostly used for things you can sink into like water or quicksand
        self.depth = 0
        
        # The entity (unit or object) in this panel
        self.entity = None
            
    # For now, all panels are flat.
    def get_north_edge_elevation(self):
        return self.elevation
    def get_south_edge_elevation(self):
        return self.elevation
    def get_east_edge_elevation(self):
        return self.elevation
    def get_west_edge_elevation(self):
        return self.elevation
    
    def get_exit_cost_for_unit(self, unit_):
        """Return the movement cost for a given unit to LEAVE this map panel.
        
        This will normally be 1, but it can be more for terrain that it is
        difficult to move through, such as deep water or mud.
        """
        # For now, always return 1.
        return 1


class Map(object):
    """Docstring"""
    
    # Value representing the movement distance to a panel that is
    # unreachable or outside a unit's movement range
    out_of_movement_range = 999
    
    def __init__(self, width, height, layers):
       
        self.map_panels = []
        """ A 3D array of MapPanels that make up this map.
        [0][0]          is the Southwest corner
        [0][height]     is the Northwest corner
        [width][0]      is the Southeast corner
        [width][height] is the Northeast corner
        The third dimension is NOT elevation.  It refers to the "layer" of
        the panel.  This is always 0, unless the panel is directly above
        another panel, in which case it is 1 (or 2, or 3, etc. if there are
        more than two panels stackedon top of each other).  Think bridges,
        lofts, balconies, etc.
        """
        
        # Initialize the map to an appropriately-sized array of MapPanels.
        # The default constructor for each map panel specifies an invalid
        # elevation.  These should be fixed on any MapPanels that are actually
        # part of the map.
        for r in range(width):
            self.map_panels.append([])
            for c in range(height):
                self.map_panels[r].append([])
                for l in range(layers):
                    self.map_panels[r][c].append(MapPanel())
        
    def get_width(self):
        return len(self.map_panels)
    def get_height(self):
        return len(self.map_panels[0])
    def get_number_of_layers(self):
        return len(self.map_panels[0][0])

    def add_entity_at_position(self, entity, x_position, y_position, layer):
        """Add an entity to the map in the given position"""
        if self.map_panels[x_position][y_position][layer].entity != None:
            # Oops!  There's already a unit there!
            return False
        self.map_panels[x_position][y_position][layer].entity = entity
        entity.current_position = (x_position, y_position, layer)
        return True
    
    def can_unit_move_in_single_step(self, unit_, from_position, to_position):
        """Return true iff a unit can move from from_position to to_position.
        
        from_position -- (x,y,layer) to begin at
        to_position -- (x,y,layer) to end at
        
        This method is only intended to be called if from_position and
        to_position are adjacent.  It does not take a unit's movement range
        into account; it only considers whether it is at all possible for
        the unit to get from one panel to the other in a single step.
        """
        from_x, from_y, from_layer = from_position
        to_x, to_y, to_layer = to_position
        # Is the unit trying to move east?
        if from_x == to_x - 1 and from_y == to_y:
            from_edge_elevation = self.map_panels[from_x][from_y][from_layer].\
                get_east_edge_elevation()
            to_edge_elevation = self.map_panels[to_x][to_y][to_layer].\
                get_west_edge_elevation()
        # Is the unit trying to move west?
        elif from_x == to_x + 1 and from_y == to_y:
            from_edge_elevation = self.map_panels[from_x][from_y][from_layer].\
                get_west_edge_elevation()
            to_edge_elevation = self.map_panels[to_x][to_y][to_layer].\
                get_east_edge_elevation()
        # Is the unit trying to move north?
        elif from_x == to_x and from_y == to_y - 1:
            from_edge_elevation = self.map_panels[from_x][from_y][from_layer].\
                get_north_edge_elevation()
            to_edge_elevation = self.map_panels[to_x][to_y][to_layer].\
                get_south_edge_elevation()
        # Is the unit trying to move south?
        elif from_x == to_x and from_y == to_y + 1:
            from_edge_elevation = self.map_panels[from_x][from_y][from_layer].\
                get_south_edge_elevation()
            to_edge_elevation = self.map_panels[to_x][to_y][to_layer].\
                get_north_edge_elevation()
        else:
            # Should never get here
            print "from_position and to_position should be adjacent"
            return False
        return abs(from_edge_elevation - to_edge_elevation) <= \
            unit_.statistics[unit.Statistic.JUMP_RANGE].get_effective_value()
    
    def calculate_movement_costs_for_unit(self, unit_):
        """Figure out which panels a unit can move to.
        
        unit -- The unit to calculate movement costs for.
        
        Return an array the same size as self.map_panels.  Each element is an
        integer representing the movement distance from the unit's current
        position to this position on the map, or -1 if the panel is out of
        range for the unit.
        
        """
        movement_costs = []
        for r in range(self.get_width()):
            movement_costs.append([])
            for c in range(self.get_height()):
                movement_costs[r].append([])
                for l in range(self.get_number_of_layers()):
                    movement_costs[r][c].append(Map.out_of_movement_range)
        bfs_queue = []
        bfs_queue.append(unit_.current_position)
        current_x, current_y, current_layer = unit_.current_position
        movement_costs[current_x][current_y][current_layer] = 0
        while len(bfs_queue) != 0:
            current_pos = bfs_queue.pop(0)
            self._cmc_bfs_visit(bfs_queue, movement_costs, current_pos, unit_)
        return movement_costs
        
    def _cmc_bfs_visit(self, bfs_queue, movement_costs, current_pos, unit_):
        """Helper function for calculate_movement_costs_for_unit"""
        # For each direction, check the following:
        # - Is the shortest path to the panel in that direction through
        #   the current panel
        # - Can the unit move from the current panel in that direction?
        # If the above two conditions are true, then update the cost to move
        # to that panel and queue up a recursive call to our bfs
        x, y, layer = current_pos
        exit_cost = self.map_panels[x][y][layer].get_exit_cost_for_unit(unit_)
        next_step_cost = movement_costs[x][y][layer] + exit_cost
        # As an optimization, don't bother looking further than the unit
        # can move.
        if next_step_cost > \
            unit_.statistics[unit.Statistic.MOVE_RANGE].get_effective_value():
            return
        next_step_positions = []
        for dest_layer in range(self.get_number_of_layers()):
            if x > 0:
                next_step_positions.append((x-1, y, dest_layer))
            if x < self.get_width() - 1:
                next_step_positions.append((x+1, y, dest_layer))
            if y > 0:
                next_step_positions.append((x, y-1, dest_layer))
            if y < self.get_height() - 1:
                next_step_positions.append((x, y+1, dest_layer))
        for next_pos in next_step_positions:
            dest_x, dest_y, dest_layer = next_pos
            check_next_pos = next_step_cost <\
                movement_costs[dest_x][dest_y][dest_layer]
            check_next_pos = check_next_pos and\
                self.can_unit_move_in_single_step\
                    (unit_, (x, y, layer),(dest_x, dest_y, dest_layer))
            if check_next_pos:
                # Update the movement cost for the next position and
                # add it to the queue
                movement_costs[dest_x][dest_y][dest_layer] = next_step_cost
                bfs_queue.append(next_pos)
