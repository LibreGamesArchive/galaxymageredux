import widget

class Label(widget.Widget):
    def __init__(self, parent, pos, text):
        widget.Widget.__init__(self, parent, pos)

        self.text = text

        self.bg_color = (1,1,1,1)

        self.size = self.get_size()

        self.text_color = (0,0,0,1)

    def get_size(self):
        return self.get_text_size(self.text)

    def render(self):
        self.size = self.get_size()
        down = 0
        if self.bg_color:
            self.draw_rect(self.get_rect(),
                           self.bg_color)
        self.draw_text(self.text, self.pos.get_pos(), self.text_color)
