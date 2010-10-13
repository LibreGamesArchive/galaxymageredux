import widget

class Button(widget.Widget):
    def __init__(self, parent, pos, text):
        widget.Widget.__init__(self, parent, pos)

        self.text = text

        self.bg_color = (1,1,1,1)

        self.size = self.get_size()

        self.text_color = (0,0,0,1)
        self.text_reg_color = (0,0,0,1)
        self.text_hover_color = (1,0,0,1)
        self.text_click_color = (1,0.5,0.5,1)

        self.dispatch.bind('hover', lambda: self.swap_text_color(self.text_hover_color))
        self.dispatch.bind('click', lambda: self.swap_text_color(self.text_hover_color))
        self.dispatch.bind('press', lambda: self.swap_text_color(self.text_click_color))
        self.dispatch.bind('press-return', lambda: self.swap_text_color(self.text_click_color))
        self.dispatch.bind('unhover', lambda: self.swap_text_color(self.text_reg_color))

    def swap_text_color(self, new):
        self.text_color = new

    def get_size(self):
        return self.get_text_size(self.text)

    def render(self):
        self.size = self.get_size()

        r = self.get_rect()
        if self.bg_color:
            self.draw_rect(r, self.bg_color)
        self.draw_text(self.text, r.topleft, self.text_color)
