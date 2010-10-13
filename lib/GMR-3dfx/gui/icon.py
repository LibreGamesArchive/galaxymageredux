import widget

class Icon(widget.Widget):
    def __init__(self, parent, pos, image):
        widget.Widget.__init__(self, parent, pos)

        self.image = image

        self.size = self.get_size()

    def get_size(self):
        return self.image.texture.size

    def render(self):
        self.image.render(self.pos.get_pos())
