import sys, os

working_dir = os.path.split(os.path.split(os.path.split(__file__)[0])[0])[0]
if not working_dir in sys.path:
    sys.path.insert(0, working_dir)

import lib
engine = lib.engine
event = lib.event

from lib.engine import *
from lib.engine.misc import Color

sys.path.pop(0)
