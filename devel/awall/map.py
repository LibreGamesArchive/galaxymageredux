"""Docstring"""

import numpy

class MapPanel:
    """Docstring"""
    
    
    def __init__(self, elevation):
        self.material = None #TODO: Implement material later
        
        # The elevation at this panel
        # TODO: How does this work with multiple corners?
        self.elevation = elevation
        
        # The depth of the terrain at this panel.
        # Mostly used for things you can sink into like water or quicksand
        self.depth = 0
        
        # The entity (unit or object) in this panel
        self.entity = None
            
    def _get_north_edge_elevation(self):
        return self.elevation
    def _get_south_edge_elevation(self):
        return self.elevation
    def _get_east_edge_elevation(self):
        return self.elevation
    def _get_west_edge_elevation( elf):
        return self.elevation
    
    north_edge_elevation = property(_get_north_edge_elevation, None)
    south_edge_elevation = property(_get_south_edge_elevation, None)
    east_edge_elevation = property(_get_east_edge_elevation, None)
    west_edge_elevation = property(_get_west_edge_elevation, None)


class Map:
    """Docstring"""
    
    
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
        
    def _get_width(self):
        width, height, layers = self.map_panels.shape
        return width
    width = property(_get_width)
    def _get_height(self):
        width, height, layers = self.map_panels.shape
        return height
    height = property(_get_height)

    def add_entity_at_position(self, entity, x_position, y_position, layer):
        self.map_panels[x_position][y_position][layer].entity = entity
        entity.current_position = (x, y, layer)
    
    def calculate_movement_costs_for_unit(self, unit_):
        """Figure out which panels a unit can move to.
        
        unit -- The unit to calculate movement costs for.
        
        Return an array the same size as self.map_panels.  Each element is an
        integer representing the movement distance from the unit's current
        position to this position on the map, or -1 if the panel is out of
        range for the unit.
        
        """
        pass