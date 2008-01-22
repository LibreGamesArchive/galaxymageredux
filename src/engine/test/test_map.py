"""Unit tests for map module"""

import map
import unit
import unittest

class MapPanelTestCase(unittest.TestCase):
    def testMapPanelEdges(self):
        """Make sure that map panel edge elevations are set properly"""
        elevation = 2
        mp = map.MapPanel(elevation)
        self.assertEquals(mp.get_north_edge_elevation(), elevation)
        self.assertEquals(mp.get_south_edge_elevation(), elevation)
        self.assertEquals(mp.get_east_edge_elevation(), elevation)
        self.assertEquals(mp.get_west_edge_elevation(), elevation)
    
    def testGetExitCostForUnit(self):
        """Make sure that the cost to exit
        a MapPanel is calculated correctly.
        """
        alice = unit.Unit("Alice", unit.Gender.FEMALE)
        mp = map.MapPanel(2)
        self.assertEquals(mp.get_exit_cost_for_unit(alice), 1)
        
class MapTestCase(unittest.TestCase):
    def setUp(self):
        self.map_ = map.Map(12, 10, 2)
        self.unit_ = unit.Unit("Unit", unit.Gender.NEUTER)
        
    def testDimensions(self):
        """Make sure that the map's dimensions are set properly."""
        self.assertEquals(self.map_.get_width(), 12)
        self.assertEquals(self.map_.get_height(), 10)
        self.assertEquals(self.map_.get_number_of_layers(), 2)
        
    def testAddEntityAtPosition(self):
        """Make sure that adding units to the map works properly"""
        e = unit.Entity("Entity")
        success = self.map_.add_entity_at_position(e, 7, 5, 0)
        assert(success)
        self.assertEquals(self.map_.map_panels[7][5][0].entity, e)
        self.assertEquals(e.current_position, (7, 5, 0))
        success = self.map_.add_entity_at_position(self.unit_, 7, 5, 0)
        assert(not success)
        success = self.map_.add_entity_at_position(self.unit_, 7, 5, 1)
        self.assertEquals(self.map_.map_panels[7][5][1].entity, self.unit_)
        self.assertEquals(self.unit_.current_position, (7, 5, 1))
        
    def testCanUnitMoveInSingleStep(self):
        """Make sure that we can determine when a unit can move to
        an adjacent panel, and when it can not."""
        self.unit_.statistics[unit.Statistic.JUMP_RANGE].base = 3
        self.map_.map_panels[1][1][0].elevation = 5
        self.map_.map_panels[0][1][0].elevation = 2  # within jump range
        self.map_.map_panels[2][1][0].elevation = 1  # too low
        self.map_.map_panels[1][0][0].elevation = 8  # within jump range
        self.map_.map_panels[1][2][0].elevation = 9  # too high
        assert(self.map_.can_unit_move_in_single_step\
            (self.unit_, (1, 1, 0), (0, 1, 0)))
        assert(not self.map_.can_unit_move_in_single_step\
            (self.unit_, (1, 1, 0), (2, 1, 0)))
        assert(self.map_.can_unit_move_in_single_step\
            (self.unit_, (1, 1, 0), (1, 0, 0)))
        assert(not self.map_.can_unit_move_in_single_step\
            (self.unit_, (1, 1, 0), (1, 2, 0)))

class MovementTestCase(unittest.TestCase):
    def setUp(self):
        self.quadratic_slope_map = map.Map(5, 5, 1)
        # Set the map elevations to column^2
        for r in range(self.quadratic_slope_map.get_width()):
            for c in range(self.quadratic_slope_map.get_height()):
                self.quadratic_slope_map.map_panels[r][c][0].elevation = c * c
        
        self.spiral_stairs_map = map.Map(3, 3, 1)
        self.spiral_stairs_map.map_panels[0][0][0].elevation = 0
        self.spiral_stairs_map.map_panels[0][1][0].elevation = 2
        self.spiral_stairs_map.map_panels[0][2][0].elevation = 4
        self.spiral_stairs_map.map_panels[1][2][0].elevation = 6
        self.spiral_stairs_map.map_panels[2][2][0].elevation = 8
        self.spiral_stairs_map.map_panels[2][1][0].elevation = 10
        self.spiral_stairs_map.map_panels[1][1][0].elevation = 12
        self.spiral_stairs_map.map_panels[1][0][0].elevation = 14
        self.spiral_stairs_map.map_panels[2][0][0].elevation = 16
        
        self.pillar_map = map.Map(3, 3, 1)
        self.pillar_map.map_panels[0][0][0].elevation = 0
        self.pillar_map.map_panels[0][1][0].elevation = 0
        self.pillar_map.map_panels[0][2][0].elevation = 0
        self.pillar_map.map_panels[1][0][0].elevation = 0
        self.pillar_map.map_panels[1][1][0].elevation = 10
        self.pillar_map.map_panels[1][2][0].elevation = 0
        self.pillar_map.map_panels[2][0][0].elevation = 0
        self.pillar_map.map_panels[2][1][0].elevation = 0
        self.pillar_map.map_panels[2][2][0].elevation = 0
        
        self.unit_ = unit.Unit("Unit", unit.Gender.NEUTER)
    
    ###
    # Remember, (0,0) is the southwest corner of the map.
    # However, because of how lists are declared below you actually
    # have to rotate the arrays 90 degrees counterclockwise to have
    # the movement cost arrays line up with the underlying map
    # representation.
    ###
    
    def testSimpleCase(self):
        """Verify that movement costs are calculated correctly"""
        self.unit_.statistics[unit.Statistic.JUMP_RANGE].base = 3
        self.unit_.statistics[unit.Statistic.MOVE_RANGE].base = 3
        self.quadratic_slope_map.add_entity_at_position(self.unit_, 0, 0, 0)
        movement_costs = self.quadratic_slope_map.\
            calculate_movement_costs_for_unit(self.unit_)
        x = map.Map.out_of_movement_range
        self.assertEqual(movement_costs,[\
            [[0], [1], [2], [x], [x]],
            [[1], [2], [3], [x], [x]],
            [[2], [3], [x], [x], [x]],
            [[3], [x], [x], [x], [x]],
            [[x], [x], [x], [x], [x]]])
        path = self.quadratic_slope_map.move_unit(self.unit_, (2, 1, 0))
        assert( 
            path == (0, 1, 0), (1, 1, 0), (2, 1, 0) or \
            path == (1, 0, 0), (1, 1, 0), (2, 1, 0) or \
            path == (1, 0, 0), (2, 0, 0), (2, 1, 0))
    def testWindingPath(self):
        """Verify that movement costs correctly take into account
        roundabout paths"""
        self.unit_.statistics[unit.Statistic.JUMP_RANGE].base = 2
        self.unit_.statistics[unit.Statistic.MOVE_RANGE].base = 8
        self.spiral_stairs_map.add_entity_at_position(self.unit_, 0, 0, 0)
        movement_costs = self.spiral_stairs_map.\
            calculate_movement_costs_for_unit(self.unit_)
        self.assertEqual(movement_costs,[\
            [[0], [1], [2]],
            [[7], [6], [3]],
            [[8], [5], [4]]])
        path = self.spiral_stairs_map.move_unit(self.unit_, (2, 0, 0))
        self.assertEqual(path, [
            (0, 1, 0),
            (0, 2, 0),
            (1, 2, 0),
            (2, 2, 0),
            (2, 1, 0),
            (1, 1, 0),
            (1, 0, 0),
            (2, 0, 0)])
    def testPillarPath(self):
        """Verify that units will take the shortest path to their destination.
        """
        self.unit_.statistics[unit.Statistic.JUMP_RANGE].base = 2
        self.unit_.statistics[unit.Statistic.MOVE_RANGE].base = 8
        self.pillar_map.add_entity_at_position(self.unit_, 0, 0, 0)
        movement_costs = self.pillar_map.\
            calculate_movement_costs_for_unit(self.unit_)
        x = map.Map.out_of_movement_range
        self.assertEqual(movement_costs,[\
            [[0], [1], [2]],
            [[1], [x], [3]],
            [[2], [3], [4]]])
        path = self.pillar_map.move_unit(self.unit_, (1, 2, 0))
        self.assertEqual(path, [
            (0, 1, 0),
            (0, 2, 0),
            (1, 2, 0)])
    
if __name__ == '__main__':
    unittest.main()