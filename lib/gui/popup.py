import widget, misc

class PopUp(widget.Widget):
    """Shows up on hover over parent"""
    widget_type = 'PopUp'
    def __init__(self, parent, pos=misc.RelativePos("left", "bottom"), text="", name=None):
        widget.Widget.__init__(self, parent.get_root_app(), pos, name)
        self.no_events = True

        self.attached_to = parent
        self.pos.to = self.attached_to
        self.text = text
        self.compile_text()

        self.attached_to.dispatch.bind("hover", self.turn_on)
        self.attached_to.dispatch.bind("unhover", self.turn_off)

    def update_theme(self):
        widget.Widget.update_theme(self)
        self.theme.set_val('visible', False)

    def turn_on(self):
        self.theme.set_val('visible', True)
        self.parent.add_widget(self)
        self.focus()
    def turn_off(self):
        self.theme.set_val('visible', False)
        self.destroy()

    def unfocus(self):
        widget.Widget.unfocus(self)
        if self.get_theme_val('visible', False):
            a,b,c,d = (self.attached_to.key_active, self.attached_to.key_hold_lengths,
                       self.attached_to._mhold, self.attached_to._mhover)
            self.parent.set_top_widget(self)
            self.attached_to.key_active, self.attached_to.key_hold_lengths = a,b
            self.attached_to._mhold, self.attached_to._mhover = c,d

    def compile_text(self):
        lines = []
        words = self.text.split(" ")

        cur_line = words[0]
        words.pop(0)
        width = self.get_theme_val('width', 100)
        while words:
            if self.get_text_size(cur_line+" "+words[0])[0] > width:
                if cur_line: lines.append(cur_line)
                cur_line = words[0]
            else:
                cur_line += " " + words[0]

            words.pop(0)

        self.comp_text = lines

    def get_size(self):
        x = self.get_theme_val('width', 100)
        y = self.get_font()[0].get_height() * len(self.comp_text)

        return x, y

    def render(self):
        pad = self.get_padding()
        x,y = self.pos.get_real_pos()
        w,h = self.get_size()

        self.draw_canvas_border((x,y,w+pad[0]+pad[2],h+pad[1]+pad[3]),
                                'background')

        font, size, color = self.get_font()
        down = font.get_height(size)

        for line in self.comp_text:
            self.draw_text(line, (x+pad[0], y+pad[1]))
            y += down

        
