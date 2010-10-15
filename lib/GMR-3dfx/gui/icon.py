import widget

class Icon(widget.Widget):
    widget_type = "Icon"
    def __init__(self, parent, pos, name=None):
        widget.Widget.__init__(self, parent, pos, name)

        self.size = self.get_size()

    def get_image(self):
        return self.theme.get_texture(self.theme.get_val('image'))

    def get_size(self):
        w,h = self.get_image().size
        pad = self.get_padding()
        return w + pad[0] + pad[2], h + pad[1] + pad[3]

    def render(self):
        i = self.get_image()
        pad = self.get_padding()
        x,y = self.pos.get_pos()
        w,h = i.size

        self.draw_rect((x+pad[0], y+pad[1], w, h), (1,1,1,1), i)
        self.draw_border((x,y,w+pad[0]+pad[2],h+pad[1]+pad[3]),
                         self.get_border())
