import widget

class Label(widget.Widget):
    widget_type = 'Label'
    def __init__(self, parent, pos, text, name=None):
        widget.Widget.__init__(self, parent, pos, name)

        self.text = text
        self.size = self.get_size()

    def get_size(self):
        return self.get_text_size(self.text)

    def render(self):
        self.size = self.get_size()
        pad = self.get_padding()
        down = 0
        x,y = self.pos.get_pos()
        w,h = self.size
        self.draw_canvas_border((x,y,w+pad[0]+pad[2],h+pad[1]+pad[3]),
                                'background', 'border')
        self.draw_text(self.text, (x+pad[0], y+pad[1]))
