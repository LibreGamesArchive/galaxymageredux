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
        down = 0
        x,y = self.pos.get_pos()
        w,h = self.size
        self.draw_canvas_border((x,y,w,h), 'background', 'border')
        self.draw_text(self.text, self.pos.get_pos())
