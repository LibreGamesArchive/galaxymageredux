import button, misc

class DropDown(button.Button):
    def __init__(self, parent, pos, text, child=None):
        button.Button.__init__(self, parent, pos, text)

        self.child = None
        if child:
            self.setChild(child)
        self.dispatch.bind('click', self.turn_on)

    def setChild(self, child):
        self.child = child
        child.pos = misc.RelativePos(to=self)
        child.dispatch.bind('unfocus', self.turn_off)
        self.turn_off()

    def turn_off(self):
        self.child.visible = False
        self.child.destroy()
    def turn_on(self):
        self.child.visible = True
        self.parent.add_widget(self.child)
