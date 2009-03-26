import pyggel, os
from pyggel import *

import net
from twisted.internet import reactor, threads, error

import ui

def load_config():
    if pyggel.misc.test_safe("data/config.txt")[0]:
        exec open("data/config.txt")
        return locals()
    else:
        raise ImportWarning("Warning, config file is not safe! Make sure no function calls or importing are present!!!")

class Game(net.Client):
    def __init__(self):
        net.Client.__init__(self, "localhost", 44444, "test!")
        self.config = load_config()
        pyggel.init(screen_size=self.config["resolution"],
                    screen_size_2d=(640, 480)) #keep 2d at 640x480

        if self.config["fullscreen"]:
            pyggel.view.toggle_fullscreen()
        pyggel.view.set_title(self.config["name"])

        self.event_handler = pyggel.event.Handler()
        self.scene = pyggel.scene.Scene()
        self.app = pyggel.gui.App(self.event_handler)
        self.message_frame = ui.MessageBox(self.app, size=(640, 400))
        pyggel.gui.NewLine(self.app)
        self.input = pyggel.gui.Input(self.app, callback=self.input_received, font_color=(1,1,1,1),
                                      width=640)
        self.scene.add_2d(self.app)

    def input_received(self, line):
        """Callback for sending out a finished line of input."""
        if line == "q":
            self.close()
        elif len(line) > 0:
            self.avatar.callRemote("sendMessage", line)
        self.get_input = True

    def update(self):
        if not self.input.key_active:
            self.input.key_active = True #make sure the input always takes, well, input...

        self.event_handler.update()
        if self.event_handler.quit:
            self.close()
            pyggel.quit()
            return None

        pyggel.view.clear_screen()
        self.scene.render()
        pyggel.view.refresh_screen()
        

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

    def remote_getMessage(self, message):
        self.message_frame.add_message(message)

def play():
    g = Game()
    g.connect()
