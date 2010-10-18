import label, container, misc

class MessageBox(container.Container):
    widget_type = 'MessageBox'
    def __init__(self, parent, size, pos, name=None):
        container.Container.__init__(self, parent, size, pos, name)

    def set_top_widget(self, widget):
        pass

    def add_line(self, text):
        label.Label(self, misc.AbsolutePos((0,0)), text)

        max_lines = self.get_theme_val('max_lines', 10)

        lasty = self.size[1]
        for i in self.widgets:
            s = i.get_size_with_padding()
            i.pos.y = lasty - s[1]
            lasty -= s[1]

        self.widgets = self.widgets[0:max_lines]
