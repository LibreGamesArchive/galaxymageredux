import button, misc

class DropDown(button.Button):
    widget_type = "DropDown"
    def __init__(self, parent, pos, text, child=None, name=None):
        button.Button.__init__(self, parent, pos, text, name)

        self.child = None
        if child:
            self.setChild(child)
        self.dispatch.bind('click', self.turn_on)
        self.dispatch.bind('unfocus', self.turn_off_vis)
        self.vis = False

    def setChild(self, child):
        self.child = child
        child.pos = misc.RelativePos(to=self)
        child.dispatch.bind('unfocus', self.turn_off)
        self.turn_off()

    def turn_off(self):
        self.child.theme.set_val('visible', False)
    def turn_off_vis(self):
        self.vis = False
    def turn_on(self):
        if self.vis:
            self.turn_off()
            self.vis = False
            return
        self.vis = True
        self.child.theme.set_val('visible', True)
