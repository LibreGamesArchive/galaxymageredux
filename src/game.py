import pyggel
from pyggel import *

import safe_python

def load_config():
    exec open("data/config.txt")
    return locals()

class Game(object):
    def __init__(self):
        self.config = load_config()
        pyggel.init((self.config["width"],
                     self.config["height"]))


def play():
    Game()
