import container, widget, misc

class ListEntry(widget.Widget):
    def __init__(self, parent, pos, text):
        widget.Widget.__init__(self, parent, pos)

        self.text = text

        self.size = self.get_size()

    def get_size(self):
        width, height = self.parent.font.get_size(self.text)
        return width, height

    def render(self):
        r = self.get_rect()
        if self.parent.entry_bg_color:
            self.draw_rect(r, self.parent.entry_bg_color)
        self.draw_text(self.text, r.topleft, self.parent.entry_bg_color)

class List(container.Container):
    def __init__(self, parent, pos, entries=[], padding=(0,0)):
        container.Container.__init__(self, parent, (1,1), pos)

        self.entry_text_color = (0,0,0,1)
        self.entry_bg_color = (1,1,1,1)

        self.entries = entries
        self.padding = padding

        self.build_entries()

    def build_entries(self):
        self.widgets = []
        width = 0
        height = 0

        for opt in self.entries:
            if self.widgets:
                pos = RelativePos(pady=self.padding[1])
            else:
                pos = AbsolutePos(self.padding)
            new = ListEntry(self, pos, opt)

            width = max(width, new.get_size()[0]+self.padding[0])
            height = new.pos.get_pos()[1]+new.get_size()[1]


        for i in self.widgets:
            i.size = width, i.size[1]

        self.change_size((width, height))
