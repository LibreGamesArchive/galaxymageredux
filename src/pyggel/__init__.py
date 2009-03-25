"""
pyggle.__init__
This library (PYGGEL) is licensed under the LGPL by Matthew Roe and PYGGEL contributors.
"""

from include import *

import mesh, view, image, camera, math3d, light
import scene, font, geometry, misc, picker, data
import particle, event, gui

def quit():
    """Deinitialize PYGGEL..."""
    view.clear_screen()
    glFlush()
    pygame.quit()

init = view.init

def get_events():
    """Return (for now) generated pygame events..."""
    return pygame.event.get()
