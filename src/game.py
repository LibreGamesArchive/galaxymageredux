import pyggel, os
from pyggel import *

import net
from twisted.internet import reactor, threads, error

def load_config():
    exec open("data/config.txt")
    return locals()

class Game(net.Client):
    def __init__(self):
        net.Client.__init__(self, "localhost", 44444, "test!")
        self.config = load_config()
        pyggel.init((800, 600))

        if self.config["fullscreen"]:
            pyggel.view.toggle_fullscreen()
        pyggel.view.set_title(self.config["name"])

        self.get_input = True

    def input_received(self, line):
        """Callback for sending out a finished line of input."""
        if line == "q":
            self.close()
        elif len(line) > 0:
            self.avatar.callRemote("sendMessage", line)
        self.get_input = True

    def update(self):
        # Only run this code once at a time!
        if self.get_input:
            # Thread this blocking call, which immediately returns a deferred
            d = threads.deferToThread(raw_input, ":->")

            # Execute function as soon as input is available
            d.addCallback(self.input_received)
            self.get_input = False

    def errHandler(self, failure):
        e = failure.trap(error.ConnectionRefusedError)
        if e == error.ConnectionRefusedError:
            self.hostname = raw_input(self.hostname + " refused connection, Alternate server hostname:")
            if hostname == '':
                self.shutdown(failure)
            self.connect() # maybe make a reconnect method?
        else:
            print "Unexpected failure: "
            self.shutdown(failure)

def play():
    g = Game()
    g.connect()
