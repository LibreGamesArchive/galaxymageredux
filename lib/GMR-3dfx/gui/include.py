import sys, os

working_dir = os.path.split(os.path.split(__file__)[0])[0]
if not working_dir in sys.path:
    sys.path.append(working_dir)

import engine
from engine import *
from engine.misc import Color

import event
