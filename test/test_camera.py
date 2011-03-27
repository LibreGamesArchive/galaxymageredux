''' Robert Ramsay
This is a small test suite for the camera module. Through a combination of 
unittest and interactive tests.
'''

import sys
sys.path.insert('..')

import unittest
from lib.engine.camera import Camera

class CameraTest(unittest.TestCase):
    '''This tests the mechanics and mathematics of the 3D camera.'''
    def TestMatrixPush(self):
        '''Tests pushing the matrix'''
        self.assertFail()
    def TestMatrixPop(self):
        '''Tests popping the matrix'''
        self.assertFail()
    def TestViewRotate(self):
        '''Tests rotating the camera'''
        self.assertFail()
    def TestViewOffset(self):
        '''Tests translating the offset'''
        self.assertFail()
    def TestPushFacingMatrix(self):
        '''Tests forcing the object in view to face the camera.'''
        self.assertFail()

def CameraTestInteractive(unittest.TestCase):
    '''Creates an opengl context and takes user feedback to ensure that the 
    camera methods act correctly'''
    def TestRotateRight(self):
        '''Rotates the camera to the right and/or the object to the left.'''
        self.assertFail()
    def TestRotateLeft(self):
        '''Rotates the camera to the left and/or the object to the right.'''
        self.assertFail()
    def TestOffsetOut(self):
        '''Zooms away from the focus.'''
        self.assertFail()
    def TestOffsetIn(self):
        '''Zooms in to the focus point.'''
        self.assertFail()
    def TestOffsetRight(self):
        '''Pans to the right.'''
        self.assertFail()
    def TestOffsetLeft(self):
        '''Pans to the left.'''
        self.assertFail()
    def TestOffsetNorth(self):
        '''Pans up the map.'''
        self.assertFail()
    def TestOffsetSouth(self):
        '''Pans down the map.'''
        self.assertFail()

if __name__ = '__main__':
    unittest.run()

