import pyggel
from pyggel import *

class MessageBox(pyggel.gui.Frame):
    def __init__(self, app, num_messages=20, **kwargs):
        pyggel.gui.Frame.__init__(self, app, **kwargs)
        self.num_messages = num_messages

        self.theme = pyggel.gui.Theme(self)
        self.theme.theme["Label"]["font-color-inactive"] = (1,1,1,1)

        self.packer.pack_upwards = self.pack_upwards
        self.packer.packtype = "upwards"
        self._messages = []

    def pack_upwards(self):
        bottom = self.size[1]
        self.widgets.reverse() #flip them!
        for i in self.widgets:
            pos = (0, bottom-i.size[1])
            bottom -= i.size[1]
            i.force_pos_update(pos)
        self.widgets.reverse()

    def add_message(self, message):
        x = pyggel.gui.Label(self, message)
        self._messages.append(x)
        if len(self.widgets) > self.num_messages:
            x = self._messages[0]
            self.widgets.remove(x)
            self._messages.remove(x)
