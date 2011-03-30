''' Robert Ramsay
This is a small test suite for the camera module. Through a combination of 
unittest and interactive tests.
'''

import sys
sys.path.insert(0, '..')

from lib.engine.camera import Camera
import pygame
from pygame.locals import *

from lib import gfx_engine, event, mod_base

import OpenGL
import unittest
from OpenGL.GL import *
from OpenGL.GLU import *

class TestCamera(unittest.TestCase):
    '''This tests the mechanics and mathematics of the 3D camera.'''
    def test_matrix_push(self):
        '''Tests pushing the matrix'''
        cam = Camera()
        depth = glGetInteger(GL_MODELVIEW_STACK_DEPTH)
        cam.push()
        glTranslate(1,1,1)
        self.assertEqual(depth + 1, glGetInteger(GL_MODELVIEW_STACK_DEPTH))
        self.assertGreater(0, glGetInteger(GL_MODELVIEW_STACK_DEPTH))
    def test_matrix_pop(self):
        '''Tests popping the matrix'''
        self.fail()
    def test_view_rotate(self):
        '''Tests rotating the camera'''
        self.fail()
    def test_view_offset(self):
        '''Tests translating the offset'''
        self.fail()
    def test_push_facing_matrix(self):
        '''Tests forcing the object in view to face the camera.'''
        self.fail()

class TestCameraInteractive(unittest.TestCase):
    '''Creates an opengl context and takes user feedback to ensure that the 
    camera methods act correctly'''
    def test_rotate_right(self):
        '''Rotates the camera to the right and/or the object to the left.'''
        self.fail()
    def test_rotate_left(self):
        '''Rotates the camera to the left and/or the object to the right.'''
        self.fail()
    def test_offset_out(self):
        '''Zooms away from the focus.'''
        self.fail()
    def test_offset_in(self):
        '''Zooms in to the focus point.'''
        self.fail()
    def test_offset_right(self):
        '''Pans to the right.'''
        self.fail()
    def test_offset_left(self):
        '''Pans to the left.'''
        self.fail()
    def test_offset_north(self):
        '''Pans up the map.'''
        self.fail()
    def test_offset_south(self):
        '''Pans down the map.'''
        self.fail()

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((640,480))
    unittest.main()

