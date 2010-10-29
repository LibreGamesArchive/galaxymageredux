import container, widget, misc

class ListEntry(widget.Widget):
    widget_type = "Entry"
    def __init__(self, parent, pos, text):
        widget.Widget.__init__(self, parent, pos, None)

        self.size = self.get_text_size(text)

        self.text = text

    def get_size(self):
        return self.size

    def check_size(self):
        self.size = self.get_text_size(self.text)

    def render(self):
        pad = self.get_padding()
        down = 0
        x,y = self.get_pos()
        w,h = self.get_size()
        self.draw_canvas_border((x,y,w+pad[0]+pad[2],h+pad[1]+pad[3]),
                                'background')
        self.draw_text(self.text, (x+pad[0], y+pad[1]))

class List(container.Container):
    widget_type = "List"
    def __init__(self, parent, pos, entries=[], name=None):
        container.Container.__init__(self, parent, (1,1), pos, name)

        self.entries = entries

        self.build_entries()

    def build_entries(self):
        self.widgets = []
        width = 0
        height = 0

        for opt in self.entries:
            if self.widgets:
                pos = misc.RelativePos()
            else:
                pos = misc.AbsolutePos((0,0))
            new = ListEntry(self, pos, opt)

        self.check_size()

    def check_size(self):
        width = 0
        height = 0
        for opt in self.widgets:
            opt.check_size()
            s = opt.get_size_with_padding()
            width = max((width, s[0]))
            height += s[1]

        for i in self.widgets:
            i.size = width, i.size[1]

        p = self.theme.get_element("Entry").get_val('padding', (0,0,0,0))

        self.change_size((width+p[0]+p[1], height))

    def update_child_theme(self):
        container.Container.update_child_theme(self)
        self.check_size()
