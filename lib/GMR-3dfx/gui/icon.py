import widget

class Icon(widget.Widget):
    widget_type = "Icon"
    def __init__(self, parent, pos, name=None):
        widget.Widget.__init__(self, parent, pos, name)

        self.size = self.get_size()

    def get_image(self):
        return self.theme.get_texture(self.theme.get_val('image'))

    def get_size(self):
        return self.get_image().size

    def render(self):
        i = self.get_image()
        x,y = self.pos.get_pos()
        w,h = i.size
        self.draw_rect((x, y, w, h), (1,1,1,1), i)
