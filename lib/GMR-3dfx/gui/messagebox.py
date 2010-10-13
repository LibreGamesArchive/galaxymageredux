import widget, container

class MessageBoxLabel(widget.Widget):
    def __init__(self, parent, text):
        widget.Widget.__init__(self, parent, (0,0))

        self.text = text

        self.size = self.get_size()

    def get_size(self):
        return self.font.get_size(self.text)

    def render(self):
        self.size = self.get_size()
        if self.parent.entry_bg_color:
            self.draw_rect(self.get_rect(),
                           self.parent.entry_bg_color)
        self.draw_text(self.text, self.pos.get_pos(), self.parent.text_color)

class MessageBox(container.Container):
    def __init__(self, parent, size, pos, max_lines=10):
        container.Container.__init__(self, parent, size, pos)

        self.max_lines = max_lines
        self.text_color = (0,0,0)
        self.entry_bg_color = None

    def add_line(self, text):
        MessageBoxLabel(self, text)

        height = self.font.get_height()

        lasty = self.size[1] - height
        for i in self.widgets:
            i.pos.y = lasty
            lasty -= height

        self.widgets = self.widgets[0:self.max_lines]
