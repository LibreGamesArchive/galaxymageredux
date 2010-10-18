import widget

class Button(widget.Widget):
    widget_type = "Button"
    def __init__(self, parent, pos, text, name=None):
        widget.Widget.__init__(self, parent, pos, name)

        self.text = text

    def get_size(self):
        return self.get_text_size(self.text)

    def render(self):
        pad = self.get_padding()
        down = 0
        x,y = self.get_pos()
        w,h = self.get_size()
        self.draw_canvas_border((x,y,w+pad[0]+pad[2],h+pad[1]+pad[3]),
                                'background')
        self.draw_text(self.text, (x+pad[0], y+pad[1]))
